from app import app
from models import db, User, Course, Quiz, CourseEnrollment, Submission

with app.app_context():
    # Find all quizzes that have submissions
    submissions = Submission.query.all()
    quiz_ids_with_submissions = set(sub.quiz_id for sub in submissions)
    
    print("Quizzes with submissions:")
    for quiz_id in quiz_ids_with_submissions:
        quiz = Quiz.query.get(quiz_id)
        if quiz:
            course = Course.query.get(quiz.course_code)
            submissions_count = Submission.query.filter_by(quiz_id=quiz_id).count()
            print(f"  Quiz ID {quiz_id}: {quiz.name} (Course: {course.code if course else 'None'}, Submissions: {submissions_count})")
    
    # Let's test with a quiz that has submissions
    if quiz_ids_with_submissions:
        test_quiz_id = list(quiz_ids_with_submissions)[0]
        quiz = Quiz.query.get(test_quiz_id)
        course = Course.query.get(quiz.course_code)
        submission = Submission.query.filter_by(quiz_id=test_quiz_id).first()
        student = User.query.get(submission.user_id)
        
        print(f"\nTest case:")
        print(f"  Quiz: {quiz.name} (ID: {quiz.id})")
        print(f"  Course: {course.code}")
        print(f"  Student: {student.username}")
        print(f"  Expected URL: /course/{course.code}/quiz/{quiz.id}/results")