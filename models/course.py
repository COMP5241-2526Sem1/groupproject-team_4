from database import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)  # Course's department
    department = db.relationship('Department', backref='courses')
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    credit = db.Column(db.Integer, default=3, nullable=False)      # Credit
    capacity = db.Column(db.Integer, nullable=False)               # Maximum capacity
    day_of_week = db.Column(db.String(10), nullable=False)         # Day of the week, e.g., 'Mon', 'Tue', 'Wed' ...
    start_time = db.Column(db.Time, nullable=False)                # Start time, e.g., 09:00:00
    end_time = db.Column(db.Time, nullable=False)                  # End time, e.g., 11:00:00

    enrollments = db.relationship('CourseEnrollment', backref='course', lazy=True)
    activities = db.relationship('Activity', backref='course', lazy=True)
    grades = db.relationship('Grade', backref='course', lazy=True)
