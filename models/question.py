from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from database import db


class Question(db.Model):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey('quiz.id'), nullable=False)
    type = Column(Enum('mcq', 'saq', name='question_type_enum'), nullable=False)
    content = Column(String(1000), nullable=False)
    points = Column(Integer, default=1)

    choices = relationship('Choice', backref='question', cascade='all, delete-orphan')