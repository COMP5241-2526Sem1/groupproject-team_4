from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import db

class Minigame(db.Model):
    __tablename__ = 'minigame'

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
    sessions = relationship('MinigameSession', backref='minigame', cascade='all, delete-orphan')
    course = relationship('Course', backref='minigames')
    creator = relationship('User', backref='created_minigames')

class MinigameSession(db.Model):
    __tablename__ = 'minigame_session'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('minigame.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    score = Column(Integer, default=0)
    state = Column(JSON)
    started_at = Column(DateTime, default=db.func.current_timestamp())
    completed_at = Column(DateTime)