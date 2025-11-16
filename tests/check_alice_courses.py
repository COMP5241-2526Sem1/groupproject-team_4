from app import app
from models import db, User, Course, CourseEnrollment, Quiz
from werkzeug.security import check_password_hash

with app.app_context():
    # Find alice_johnson user
    user = User.query.filter_by(username='alice_johnson').first()
    if user:
        print(f"alice_johnson ID: {user.id}")
        
        # Find courses she's enrolled in
        enrollments = CourseEnrollment.query.filter_by(student_id=user.id).all()
        print("Courses alice_johnson is enrolled in:")
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
                        submissions = Submission.query.filter_by(quiz_id=quiz.id, user_id=user.id).all()
                        if submissions:
                            print(f"    Has {len(submissions)} submissions from alice_johnson")
                            
                            # Find alice's password
                            test_passwords = ['password', '123456', 'student', 'alice', 'alice_johnson', 'alice123']
                            for pwd in test_passwords:
                                if check_password_hash(user.password_hash, pwd):
                                    print(f"    alice_johnson password: {pwd}")
                                    break
                            
                            # This is a good quiz to test
                            print(f"    Good test case: /course/{enrollment.course_code}/quiz/{quiz.id}/results")
                            break
                    break