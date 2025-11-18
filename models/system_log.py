from models import db
from datetime import datetime

class SystemLog(db.Model):
    __tablename__ = 'system_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100))
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
