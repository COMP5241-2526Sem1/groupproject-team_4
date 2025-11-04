from . import db

class Department(db.Model):
    __tablename__ = 'department'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), nullable=False, unique=True)          # Department code (e.g., 'COMP')
    full_name = db.Column(db.String(100), nullable=False)                # Full department name (e.g., 'Department of Computer Science')