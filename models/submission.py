from models import db
from datetime import datetime
from sqlalchemy import JSON, Enum

class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    answer = db.Column(JSON)  # 保持兼容性，同时作为 answer_raw 的别名
    answer_raw = db.Column(JSON)  # 学生的原始回答（JSON格式）
    score = db.Column(db.Float)
    is_correct = db.Column(db.Boolean)  # 对于quiz等可判断正确性的活动
    status = db.Column(Enum('submitted', 'graded', 'in_review', 'returned'), default='submitted')
    feedback = db.Column(db.Text)  # 教师评语
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    graded_at = db.Column(db.DateTime)  # 评分时间

