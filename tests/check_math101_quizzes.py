# Check if there are any quizzes in MATH101
from models import User, Quiz, CourseEnrollment, Attempt
from database import db
from app import app

with app.app_context():
    # Find carol_davis
    user = User.query.filter_by(username='carol_davis').first()
    if not user:
        print("User not found")
        exit(1)
    
    print(f"User: {user.username} (ID: {user.id}, Role: {user.role})")
    
    # Find quizzes in MATH101
    math101_quizzes = Quiz.query.filter_by(course_code='MATH101').all()
    print(f"Quizzes in MATH101: {len(math101_quizzes)}")
    
    for quiz in math101_quizzes:
        attempts = Attempt.query.filter_by(user_id=user.id, quiz_id=quiz.id).count()
        print(f"  Quiz {quiz.id}: {quiz.name} - User attempts: {attempts}")
    
    # Check if we can enroll carol_davis in COMP201
    comp201_enrollment = CourseEnrollment.query.filter_by(student_id=user.id, course_code='COMP201').first()
    if comp201_enrollment:
        print("Already enrolled in COMP201")
    else:
        print("Not enrolled in COMP201")
        
        # Check if we can create an enrollment
        from datetime import datetime
        new_enrollment = CourseEnrollment(
            course_code='COMP201',
            student_id=user.id,
            enrolled_at=datetime.utcnow()
        )
        db.session.add(new_enrollment)
        try:
            db.session.commit()
            print("Successfully enrolled in COMP201")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to enroll in COMP201: {e}")
            
        # Check enrollment again
        comp201_enrollment = CourseEnrollment.query.filter_by(student_id=user.id, course_code='COMP201').first()
        if comp201_enrollment:
            print("Now enrolled in COMP201")
        else:
            print("Still not enrolled in COMP201")