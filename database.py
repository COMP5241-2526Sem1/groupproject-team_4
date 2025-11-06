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
            from models.department import Department
            from models.user import User

            from models.submission import Submission
            from models.quiz import Quiz
            from models.poll import Poll
            from models.word_cloud import WordCloud
            from models.minigame import Minigame
            from models.short_answer import ShortAnswer
            from models.question import Question

            from models.grade import Grade
            from models.course_enrollment import CourseEnrollment
            from models.course import Course
            from models.choice import Choice

            models = [Department, User, Submission, Quiz, Poll, WordCloud, Minigame, ShortAnswer, Question, Grade, CourseEnrollment, Course, Choice]
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
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role user_role_enum NOT NULL,
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    department_code VARCHAR(10) REFERENCES department(name)
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