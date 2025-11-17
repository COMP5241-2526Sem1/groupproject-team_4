from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import db


class Submission(db.Model):
    __tablename__ = 'submission'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
    # Task type foreign keys (only one should be set)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=True)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=True)
    short_answer_id = Column(Integer, ForeignKey('short_answer.id'), nullable=True)
    word_cloud_id = Column(Integer, ForeignKey('word_cloud.id'), nullable=True)
    minigame_id = Column(Integer, ForeignKey('minigame.id'), nullable=True)
    
    submitted_at = Column(DateTime, default=func.now())
    grade = Column(Float)

    # Relationships
    question_responses = db.relationship('QuestionResponse', backref='submission', cascade='all, delete-orphan')