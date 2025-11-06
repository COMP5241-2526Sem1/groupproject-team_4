from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import db


class Quiz(db.Model):
    __tablename__ = 'quiz'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(500))
    is_graded = Column(Boolean, default=False)
    visibility = Column(Enum('public', 'private', name='visibility_enum'), default='public')
    attempt_limit = Column(Integer, default=1)
    duration = Column(Integer, default=30)  # Duration in minutes
    created_at = Column(db.DateTime, default=func.now())
    updated_at = Column(db.DateTime, default=func.now(), onupdate=func.now())

    questions = relationship('Question', backref='quiz', cascade='all, delete-orphan')