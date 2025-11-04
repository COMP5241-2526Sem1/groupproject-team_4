from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import db


class Attempt(db.Model):
    __tablename__ = 'attempt'

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    attempt_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # 关联关系
    quiz = relationship('Quiz', backref='attempts')
    user = relationship('User', backref='attempts')