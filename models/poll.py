from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import db

class Poll(db.Model):
    __tablename__ = 'poll'

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
    point = Column(Integer, default=0)  # Polls are ungraded
    point_in_course = Column(Integer, default=0)

    # Visibility settings - polls should be always visible
    after_submitted_question_visible = Column(Boolean, default=True)
    after_submitted_student_response_visible = Column(Boolean, default=True)
    after_submitted_sample_response_visible = Column(Boolean, default=True)
    after_submitted_class_response_visible = Column(Boolean, default=True)

    # Relationships
    questions = relationship("Question", backref="poll", cascade="all, delete-orphan",
                           foreign_keys='Question.poll_id')
    course = relationship('Course', backref='polls')
    creator = relationship('User', backref='created_polls')