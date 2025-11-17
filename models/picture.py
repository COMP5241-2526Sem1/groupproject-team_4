from sqlalchemy import Column, Integer, String, Text, LargeBinary, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import db

class Picture(db.Model):
    __tablename__ = 'picture'
    
    id = Column(Integer, primary_key=True)
    minigame_id = Column(Integer, ForeignKey('minigame.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    filename = Column(String(255), nullable=False)
    file_data = Column(LargeBinary, nullable=False)
    file_type = Column(String(50), nullable=False)  # e.g., 'image/jpeg', 'image/png'
    file_size = Column(Integer, nullable=False)  # in bytes
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<Picture {self.filename}>'