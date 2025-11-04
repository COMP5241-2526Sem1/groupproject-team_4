from sqlalchemy import Column, Integer, String, DateTime, JSON
from database import db

class Minigame(db.Model):
    __tablename__ = 'minigame'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    config = Column(JSON)

class MinigameSession(db.Model):
    __tablename__ = 'minigame_session'

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('minigame.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    score = Column(Integer, default=0)
    state = Column(JSON)
    started_at = Column(DateTime, default=db.func.current_timestamp())
    completed_at = Column(DateTime)