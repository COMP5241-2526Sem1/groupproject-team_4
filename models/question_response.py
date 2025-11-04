from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Float
from database import db

# user response to ONE question
class QuestionResponse(db.Model):
    __tablename__ = 'question_response'

    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey('submission.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    # if mcq, content is user choice(eg, A or ABD)
    # if saq, content is some text
    content = Column(Text)
    is_correct = Column(Boolean)
    points = Column(Float, default=0.0)