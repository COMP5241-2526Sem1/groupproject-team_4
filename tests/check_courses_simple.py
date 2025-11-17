from app import app
from models import Course, User

with app.app_context():
    courses = Course.query.all()
    print('Available courses:')
    for course in courses:
        teacher = User.query.get(course.teacher_id)
        teacher_name = teacher.username if teacher else 'Unknown'
        print(f'{course.code}: {course.name} (Teacher: {teacher_name})')
    
    if not courses:
        print('No courses found in database!')