from pathlib import Path
import sys
import unittest
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import text
from database import db
from models import Course, CourseEnrollment, User
from werkzeug.security import generate_password_hash, check_password_hash


class TestGetMyCourses(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object(Config)
        self.app.config['TESTING'] = True
        
        self.app.secret_key = 'test_secret_key'
        db.init_app(self.app)
        try:
            db.session.execute(text('SELECT version();'))
            print("PostgreSQL Database Connected Successfully!!!")
        except Exception as e:
            print(f"PostgreSQL Database Connection Failed!: {e}")
        from routes.auth import auth_bp
        from routes.course import course_bp
        self.app.register_blueprint(course_bp)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        # make sure all the tables are correct
        db.create_all()

        # Insert test data
        self.user = User(id=200, username='testuser123', password=generate_password_hash('Testpass123'))
        db.session.add(self.user)

    def tearDown(self):
        db.session.remove()
        self.app_context.pop()

    def test_not_logged_in(self):
        # Simulate not logged in state
        with self.client as c:
            response = c.get('/courses/my')
            self.assertEqual(response.status_code, 401)
            self.assertEqual(response.json, {'msg': 'Not logged in'})

    def test_no_enrolled_courses(self):
        # Simulate logged in but no courses selected
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 200  # Simulate user login
            response = c.get('/courses/my')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, [])

    def test_get_available_courses(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 200  # Simulate user login
        # Test getting available courses
        with self.client as c:
            response = c.get('/courses/available')
            print("Response:", response.json)  # Print response
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json, list)

    def test_with_enrolled_courses(self):
        # Simulate logged in with courses selected
        enrollment = CourseEnrollment(user_id=200, course_id=1)
        db.session.add(enrollment)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 200  # Simulate user login
            response = c.get('/courses/my')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 1)
            self.assertEqual(response.json[0]['name'], "Math")
            self.assertEqual(response.json[0]['day_of_week'], "Mon")

    def test_add_course(self):
        # Simulate adding course
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1  # Simulate user login
            response = c.post('/courses/add', json={'course_id': 1})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'msg': 'Course added successfully'})

            # Verify course list contains newly added course
            response = c.get('/courses/my')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 1)
            self.assertEqual(response.json[0]['name'], "Math")

    def test_drop_course(self):
        # Simulate deleting course
        enrollment = CourseEnrollment(user_id=1, course_id=1)
        db.session.add(enrollment)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1  # Simulate user login
            response = c.post('/courses/drop', json={'course_id': 1})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'msg': 'Course dropped successfully'})

            # Verify course list has removed the course
            response = c.get('/courses/my')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json), 0)


if __name__ == '__main__':
    unittest.main()