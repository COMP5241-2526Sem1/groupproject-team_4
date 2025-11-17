from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import db


class ShortAnswer(db.Model):
    __tablename__ = 'short_answer'
    
    id = Column(Integer, primary_key=True)
    course_code = Column(String(20), ForeignKey('course.code'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=func.now())
    start_datetime = Column(DateTime, nullable=True)
    end_datetime = Column(DateTime, nullable=True)
    duration = Column(Integer, default=30)
    attempt_limit = Column(Integer, default=5)
    point = Column(Integer, default=100)
    point_in_course = Column(Integer, default=0)
    
    # Relationship to questions
    questions = relationship('Question', backref='short_answer', cascade='all, delete-orphan',
                           foreign_keys='Question.short_answer_id')
    course = relationship('Course', backref='short_answers')
    creator = relationship('User', backref='created_short_answers')
