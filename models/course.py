from models import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    credit = db.Column(db.Integer, default=3, nullable=False)      # 学分
    capacity = db.Column(db.Integer, nullable=False)               # 最大人数
    day_of_week = db.Column(db.String(10), nullable=False)         # 星期几，如 'Mon', 'Tue', 'Wed' ...
    start_time = db.Column(db.Time, nullable=False)                # 开始时间，如 09:00:00
    end_time = db.Column(db.Time, nullable=False)                  # 结束时间，如 11:00:00

    enrollments = db.relationship('CourseEnrollment', backref='course', lazy=True)
    activities = db.relationship('Activity', backref='course', lazy=True)
    grades = db.relationship('Grade', backref='course', lazy=True)
