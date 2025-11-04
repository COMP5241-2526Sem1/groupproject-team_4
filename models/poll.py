from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import db

class Poll(db.Model):
    __tablename__ = 'poll'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=db.func.current_timestamp())
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)

    # 关联到Question模型，与Quiz类似的关系
    questions = relationship("Question", backref="poll", cascade="all, delete-orphan")