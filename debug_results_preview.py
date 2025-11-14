from database import db
from models.user import User
from models.course import Course
from models.course_enrollment import CourseEnrollment
from models.quiz import Quiz
from models.submission import Submission
from models.attempt import Attempt
from datetime import datetime
from flask import Flask
from app import app

def debug_results_preview():
    """Debug the results preview logic"""
    
    # Test with student 31 and quiz 4
    user_id = 31
    quiz_id = 4
    course_code = 'COMP101'
    
    print("=== Debug Results Preview Logic ===")
    print(f"User ID: {user_id}")
    print(f"Quiz ID: {quiz_id}")
    print(f"Course Code: {course_code}")
    print()
    
    # Get user
    user = User.query.get(user_id)
    print(f"User: {user.username} (Role: {user.role})")
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    print(f"Quiz: {quiz.name}")
    print(f"Attempt Limit: {quiz.attempt_limit}")
    print(f"Visibility Settings:")
    print(f"  - Question Visible: {quiz.after_submitted_question_visible}")
    print(f"  - Student Response Visible: {quiz.after_submitted_student_response_visible}")
    print(f"  - Sample Response Visible: {quiz.after_submitted_sample_response_visible}")
    print(f"  - Class Response Visible: {quiz.after_submitted_class_response_visible}")
    print()
    
    # Get attempt count
    attempt_count = Attempt.query.filter_by(quiz_id=quiz_id, user_id=user_id).count()
    print(f"Attempt Count: {attempt_count}")
    
    # Check if user can attempt
    is_teacher = user and user.role == 'teacher'
    can_attempt = is_teacher or not quiz.attempt_limit or attempt_count < quiz.attempt_limit
    print(f"Is Teacher: {is_teacher}")
    print(f"Can Attempt: {can_attempt}")
    print()
    
    # Check submission
    submission = Submission.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
    has_submission = submission is not None
    print(f"Has Submission: {has_submission}")
    
    if submission:
        print(f"Submission ID: {submission.id}")
        print(f"Grade: {submission.grade}")
        print(f"Submitted At: {submission.submitted_at}")
    print()
    
    # Check results preview conditions
    should_show_preview = (
        has_submission and 
        not can_attempt and 
        (quiz.after_submitted_question_visible or 
         quiz.after_submitted_student_response_visible or 
         quiz.after_submitted_sample_response_visible or 
         quiz.after_submitted_class_response_visible)
    )
    
    print(f"Should Show Results Preview: {should_show_preview}")
    
    if should_show_preview:
        print("✅ All conditions met for results preview!")
    else:
        print("❌ Conditions not met:")
        if not has_submission:
            print("  - No submission found")
        if can_attempt:
            print("  - User can still attempt (quiz not completed)")
        if not (quiz.after_submitted_question_visible or 
                quiz.after_submitted_student_response_visible or 
                quiz.after_submitted_sample_response_visible or 
                quiz.after_submitted_class_response_visible):
            print("  - No visibility flags are enabled")
    
    # Also check for other submissions
    all_submissions = Submission.query.filter_by(quiz_id=quiz_id).all()
    print(f"\nTotal submissions for this quiz: {len(all_submissions)}")
    for sub in all_submissions:
        print(f"  - User {sub.user_id}: Grade {sub.grade}, Date {sub.submitted_at}")

if __name__ == "__main__":
    with app.app_context():
        debug_results_preview()