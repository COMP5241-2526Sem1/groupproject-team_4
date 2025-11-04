from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.sql import func
from database import db


class Submission(db.Model):
    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activity.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    submitted_at = Column(db.DateTime, default=func.now())
    grade = Column(Float)

    answers = db.relationship('Answer', backref='submission', cascade='all, delete-orphan')