# Check what courses and quizzes carol_davis has access to
from models import User, Course, Quiz, CourseEnrollment
from database import db
from app import app
import json

with app.app_context():
    # Find carol_davis
    user = User.query.filter_by(username='carol_davis').first()
    if not user:
        print("User not found")
        exit(1)
    
    print(f"User: {user.username} (ID: {user.id}, Role: {user.role})")
    
    # Find enrolled courses
    enrollments = CourseEnrollment.query.filter_by(student_id=user.id).all()
    print(f"Enrolled courses: {len(enrollments)}")
    
    for enrollment in enrollments:
        course = Course.query.filter_by(code=enrollment.course_code).first()
        if course:
            print(f"  Course: {course.code} - {course.name}")
            
            # Find quizzes for this course
            quizzes = Quiz.query.filter_by(course_code=course.code).all()
            print(f"    Quizzes: {len(quizzes)}")
            for quiz in quizzes:
                print(f"      Quiz {quiz.id}: {quiz.title}")
                
                # Check attempts
                from models import Attempt
                attempts = Attempt.query.filter_by(user_id=user.id, quiz_id=quiz.id).all()
                print(f"      Attempts: {len(attempts)}")
                if attempts:
                    for attempt in attempts:
                        print(f"        Attempt {attempt.id}: Score {attempt.score}")