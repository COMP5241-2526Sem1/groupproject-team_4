from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import db


class Question(db.Model):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    # Task type foreign keys (only one should be set)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=True)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=True)
    short_answer_id = Column(Integer, ForeignKey('short_answer.id'), nullable=True)
    word_cloud_id = Column(Integer, ForeignKey('word_cloud.id'), nullable=True)
    minigame_id = Column(Integer, ForeignKey('minigame.id'), nullable=True)
    
    type = Column(Enum('mcq', 'saq', name='question_type_enum'), nullable=False)
    content = Column(String(1000), nullable=False)
    points = Column(Integer, default=1)

    choices = relationship('Choice', backref='question', cascade='all, delete-orphan')