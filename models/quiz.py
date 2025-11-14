from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import db


class Quiz(db.Model):
    __tablename__ = 'quiz'

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
    
    # Visibility settings after submission
    after_submitted_question_visible = Column(Boolean, default=False)
    after_submitted_student_response_visible = Column(Boolean, default=False)
    after_submitted_sample_response_visible = Column(Boolean, default=False)
    after_submitted_class_response_visible = Column(Boolean, default=False)

    # Relationships
    questions = relationship('Question', backref='quiz', cascade='all, delete-orphan',
                           foreign_keys='Question.quiz_id')
    course = relationship('Course', backref='quizzes')
    creator = relationship('User', backref='created_quizzes')