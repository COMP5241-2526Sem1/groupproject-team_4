from app import app
from models import db, User, Course, Quiz, CourseEnrollment, Submission

with app.app_context():
    # Find all quizzes that have submissions
    submissions = Submission.query.all()
    
    # Group by quiz ID and count
    from collections import Counter
    quiz_submission_counts = Counter(sub.quiz_id for sub in submissions)
    
    print("Quizzes with submissions:")
    for quiz_id, count in quiz_submission_counts.items():
        quiz = Quiz.query.get(quiz_id)
        if quiz:
            course = Course.query.get(quiz.course_code)
            print(f"  Quiz ID {quiz_id}: {quiz.name} (Course: {course.code if course else 'None'}, Submissions: {count})")
            
            # Get a student who submitted to this quiz
            submission = Submission.query.filter_by(quiz_id=quiz_id).first()
            if submission:
                student = User.query.get(submission.user_id)
                print(f"    Student: {student.username if student else 'Unknown'}")
                print(f"    Expected URL: /course/{quiz.course_code}/quiz/{quiz.id}/results")
                print()