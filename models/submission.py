from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.sql import func
from database import db


class Submission(db.Model):
    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=True)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=True)
    submitted_at = Column(db.DateTime, default=func.now())
    grade = Column(Float)

    QuestionResponse = db.relationship('QuestionResponse', backref='submission', cascade='all, delete-orphan')