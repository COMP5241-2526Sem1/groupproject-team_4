from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import db


class Choice(db.Model):
    __tablename__ = 'choice'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    content = Column(String(500), nullable=False)
    is_correct = Column(Boolean, default=False)