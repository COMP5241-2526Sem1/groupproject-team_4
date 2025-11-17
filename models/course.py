from database import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'course'
    code = db.Column(db.String(20), primary_key=True)  # Course code as primary key (e.g., 'COMP1010')
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    department_code = db.Column(db.String(10), db.ForeignKey('department.name'), nullable=True)  # Course's department code
    department = db.relationship('Department', backref='courses')
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    credit = db.Column(db.Integer, default=3, nullable=False)      # Credit
    capacity = db.Column(db.Integer, nullable=False)               # Maximum capacity
    day_of_week = db.Column(db.String(10), nullable=False)         # Day of the week, e.g., 'Mon', 'Tue', 'Wed' ...
    start_time = db.Column(db.Time, nullable=False)                # Start time, e.g., 09:00:00
    end_time = db.Column(db.Time, nullable=False)                  # End time, e.g., 11:00:00
    course_number = db.Column(db.String(10), nullable=False)      # Second part of course code (e.g., '1010' from 'COMP1010')

    enrollments = db.relationship('CourseEnrollment', backref='course', lazy=True)
    grades = db.relationship('Grade', backref='course', lazy=True)
