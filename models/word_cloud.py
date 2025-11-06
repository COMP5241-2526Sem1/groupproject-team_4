from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import db

class WordCloud(db.Model):
    __tablename__ = 'word_cloud'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
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
    config = Column(JSON)
    
    # Relationships
    word_entries = relationship('WordEntry', backref='word_cloud', cascade='all, delete-orphan')
    course = relationship('Course', backref='word_clouds')
    creator = relationship('User', backref='created_word_clouds')

class WordEntry(db.Model):
    __tablename__ = 'word_entry'

    id = Column(Integer, primary_key=True)
    word_cloud_id = Column(Integer, ForeignKey('word_cloud.id'), nullable=False)
    word = Column(String(50), nullable=False)
    frequency = Column(Integer, default=1)
    submitted_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    submitted_at = Column(DateTime, default=db.func.current_timestamp())