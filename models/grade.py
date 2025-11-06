from database import db
from datetime import datetime

class Grade(db.Model):
    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), db.ForeignKey('course.code'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    grade = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
