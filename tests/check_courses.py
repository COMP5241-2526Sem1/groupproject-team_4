from app import app
from database import db
from models.course import Course
from models.user import User

with app.app_context():
    courses = Course.query.all()
    print("All courses:")
    for course in courses:
        print(f"  {course.code}: {course.name} (Teacher ID: {course.teacher_id})")
    
    # Check if debug_teacher has any courses
    debug_teacher = User.query.filter_by(username='debug_teacher').first()
    if debug_teacher:
        teacher_courses = Course.query.filter_by(teacher_id=debug_teacher.id).all()
        print(f"\nDebug teacher courses: {len(teacher_courses)}")
        for course in teacher_courses:
            print(f"  {course.code}: {course.name}")
        
        if not teacher_courses:
            print("Creating a course for debug_teacher...")
            new_course = Course(
                code='DEBUG101',
                name='Debug Course',
                description='Course for debugging',
                teacher_id=debug_teacher.id,
                course_number=101,
                department_code='COMP',
                credit=3,
                capacity=30,
                day_of_week='Mon',
                start_time='09:00:00',
                end_time='11:00:00'
            )
            db.session.add(new_course)
            db.session.commit()
            print(f"✅ Created course DEBUG101 for debug_teacher")