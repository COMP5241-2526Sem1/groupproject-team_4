from app import app
from models.user import User

with app.app_context():
    teachers = User.query.filter_by(role='teacher').all()
    for t in teachers:
        print(f'Teacher: {t.username}, {t.email}')
    
    students = User.query.filter_by(role='student').all()
    for s in students[:3]:  # Just show first 3 students
        print(f'Student: {s.username}, {s.email}')