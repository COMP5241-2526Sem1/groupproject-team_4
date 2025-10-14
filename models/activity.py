from models import db
from datetime import datetime
from sqlalchemy import Enum, JSON

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    type = db.Column(Enum('quiz', 'poll', 'wordcloud', 'short_answer', 'game'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('Submission', backref='activity', lazy=True)
