from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import db


class Answer(db.Model):
    __tablename__ = 'answer'

    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submission.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    content = Column(String(1000))
    is_correct = Column(Boolean)