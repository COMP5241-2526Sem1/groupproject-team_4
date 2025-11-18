from models import db
from datetime import datetime
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('student', 'teacher', 'admin'), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    courses = db.relationship('Course', backref='teacher', lazy=True)
    enrollments = db.relationship('CourseEnrollment', backref='student', lazy=True)
    submissions = db.relationship('Submission', backref='student', lazy=True)
    grades = db.relationship('Grade', backref='student', lazy=True)
    sent_notifications = db.relationship('Notification', foreign_keys='Notification.sender_id', backref='sender', lazy=True)
    received_notifications = db.relationship('Notification', foreign_keys='Notification.receiver_id', backref='receiver', lazy=True)
    logs = db.relationship('SystemLog', backref='user', lazy=True)
