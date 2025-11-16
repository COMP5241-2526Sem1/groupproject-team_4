from app import app
from models.user import User
from models.course import Course
from models.course_enrollment import CourseEnrollment

with app.app_context():
    # Check users
    users = User.query.all()
    print("Users:")
    for user in users:
        print(f"  {user.username}: {user.role}")
    
    # Check courses
    courses = Course.query.all()
    print("\nCourses:")
    for course in courses:
        print(f"  {course.code}: {course.name}")
    
    # Check enrollments for student 'a'
    student_a = User.query.filter_by(username='a').first()
    if student_a:
        student_enrollments = CourseEnrollment.query.filter_by(student_id=student_a.id).all()
        print(f"\nEnrollments for student 'a' (id: {student_a.id}):")
        for enrollment in student_enrollments:
            print(f"  Course: {enrollment.course_code}")
    
    # Check enrollments
    enrollments = CourseEnrollment.query.all()
    print("\nEnrollments:")
    for enrollment in enrollments:
        print(f"  Student {enrollment.student_id} in {enrollment.course_code}")