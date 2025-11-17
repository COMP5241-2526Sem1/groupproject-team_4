from app import app
from models import db, User, Course, CourseEnrollment, Quiz

with app.app_context():
    # Find debug_teacher user
    user = User.query.filter_by(username='debug_teacher').first()
    if user:
        print(f"debug_teacher ID: {user.id}")
        
        # Find courses they're enrolled in
        enrollments = CourseEnrollment.query.filter_by(student_id=user.id).all()
        print("Courses debug_teacher is enrolled in:")
        for enrollment in enrollments:
            course = Course.query.get(enrollment.course_code)
            print(f"  {enrollment.course_code}: {course.name if course else 'Unknown'}")
            
        # Find quizzes in those courses
        if enrollments:
            for enrollment in enrollments:
                quizzes = Quiz.query.filter_by(course_code=enrollment.course_code).all()
                if quizzes:
                    print(f"Quizzes in {enrollment.course_code}:")
                    for quiz in quizzes:
                        print(f"  Quiz {quiz.id}: {quiz.name}")
                        
                        # Check if there are submissions for this quiz
                        from models import Submission
                        submissions = Submission.query.filter_by(quiz_id=quiz.id).all()
                        if submissions:
                            print(f"    Has {len(submissions)} submissions")
                            
    else:
        print("debug_teacher not found")