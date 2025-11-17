from app import app, db
from models.user import User
from models.course import Course

with app.app_context():
    # Find who owns PHYS101
    phys_course = Course.query.filter_by(code='PHYS101').first()
    if phys_course:
        teacher = User.query.get(phys_course.teacher_id)
        if teacher:
            print(f'PHYS101 is owned by teacher: {teacher.username} (ID: {teacher.id})')
        else:
            print(f'PHYS101 teacher_id {phys_course.teacher_id} not found')
    else:
        print('PHYS101 course not found')