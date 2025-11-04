from sqlalchemy import Column, Integer, String, DateTime
from database import db

class WordCloud(db.Model):
    __tablename__ = 'word_cloud'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=db.func.current_timestamp())
    created_by = Column(Integer, ForeignKey('user.id'), nullable=False)

class WordEntry(db.Model):
    __tablename__ = 'word_entry'

    id = Column(Integer, primary_key=True)
    word_cloud_id = Column(Integer, ForeignKey('word_cloud.id'), nullable=False)
    word = Column(String(50), nullable=False)
    frequency = Column(Integer, default=1)
    submitted_by = Column(Integer, ForeignKey('user.id'), nullable=False)
    submitted_at = Column(DateTime, default=db.func.current_timestamp())