from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import db

class Poll(db.Model):
    __tablename__ = 'poll'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    is_multiple_choice = Column(Boolean, default=False)
    created_at = Column(DateTime, default=db.func.current_timestamp())
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)

    options = relationship("PollOption", backref="poll")

class PollOption(db.Model):
    __tablename__ = 'poll_option'

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=False)
    content = Column(String(200), nullable=False)

class PollResponse(db.Model):
    __tablename__ = 'poll_response'

    id = Column(Integer, primary_key=True)
    poll_id = Column(Integer, ForeignKey('poll.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    option_id = Column(Integer, ForeignKey('poll_option.id'), nullable=False)
    responded_at = Column(DateTime, default=db.func.current_timestamp())