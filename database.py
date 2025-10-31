import os
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy


# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize SQLAlchemy
db = SQLAlchemy()




# Test database connection
def test_db_connection():
    print("Database connection successful!")
    try:
        with app.app_context():
            db.session.execute(text('SELECT version();'))
            print("PostgreSQL Database Connected Successfully!")
    except Exception as e:
        print(f"PostgreSQL Database Connection Failed!: {e}")

# Initialize database tables
def init_db():
    try:
        with app.app_context():
            # Dynamically import models to avoid circular imports
            from models.user import Users
            from models.system_log import SystemLog
            from models.submission import Submission
            from models.quiz import Quiz
            from models.question import Question
            from models.notification import Notification
            from models.grade import Grade
            from models.course_enrollment import CourseEnrollment
            from models.course import Course
            from models.choice import Choice

            models = [Users, SystemLog, Submission, Quiz, Question, Notification, Grade, CourseEnrollment, Course, Choice]
            for model in models:
                try:
                    model.__table__.create(db.engine)
                    print(f"Table '{model.__tablename__}' created successfully.")
                except Exception as e:
                    print(f"Failed to create table '{model.__tablename__}': {e}")
    except Exception as e:
        print(f"Failed to create database tables: {e}")

# Create user table manually
def create_user_table():
    try:
        with app.app_context():
            db.session.execute(text(
                """
                CREATE TABLE IF NOT EXISTS "user" (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(80) NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            ))
            db.session.commit()
            print("User table created successfully!")
    except Exception as e:
        print(f"Failed to create user table: {e}")

if __name__ == "__main__":
    # Test database connection
    #test_db_connection()
    print("Database connection successful!")
    # Initialize database tables
    #init_db()
    print("xxx")