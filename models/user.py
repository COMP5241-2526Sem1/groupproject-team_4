from sqlalchemy import Enum, Column, Integer, String
from datetime import datetime
from database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('student', 'teacher', 'admin', name='user_role_enum'), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    department_code = db.Column(db.String(10), db.ForeignKey('department.name'), nullable=True)  # User's department code (nullable)
    department = db.relationship('Department', backref='users')

    courses = db.relationship('Course', backref='teacher', lazy=True)
    enrollments = db.relationship('CourseEnrollment', backref='student', lazy=True)
    submissions = db.relationship('Submission', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)

    