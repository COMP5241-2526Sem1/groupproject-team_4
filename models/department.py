from . import db

class Department(db.Model):
    __tablename__ = 'department'

    name = db.Column(db.String(10), primary_key=True)          # Department code as primary key (e.g., 'COMP')
    full_name = db.Column(db.String(100), nullable=False)                # Full department name (e.g., 'Department of Computer Science')