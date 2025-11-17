from database import db
from datetime import datetime

class QuizGrade(db.Model):
    __tablename__ = 'quiz_grade'
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points_earned = db.Column(db.Float, nullable=False)
    points_possible = db.Column(db.Float, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submission.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    quiz = db.relationship('Quiz', backref='quiz_grades')
    student = db.relationship('User', backref='quiz_grades')
    submission = db.relationship('Submission', backref='quiz_grade')