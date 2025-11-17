from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from database import db

# user response to ONE question
class QuestionResponse(db.Model):
    __tablename__ = 'question_response'

    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submission.id'), nullable=False)  # 通过 submission 关联到用户
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    choice_id = Column(Integer, ForeignKey('choice.id'), nullable=True)  # 用于多选题
    text_answer = Column(Text, nullable=True)  # 用于简答题
    is_correct = Column(Boolean, default=False)
    points = Column(Float, default=0.0)
    
    submission = relationship('Submission', backref='question_responses')