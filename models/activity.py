from database import db
from datetime import datetime
from sqlalchemy import Enum, JSON

class Activity(db.Model):
    __tablename__ = 'activity'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    type = db.Column(Enum('quiz', 'poll', 'wordcloud', 'short_answer', 'game', name='activity_type_enum'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submission = db.relationship('Submission', backref='activity', lazy=True)
