from app import app
from models import db, User, Course, Quiz, CourseEnrollment, Submission
import requests

# Test the quiz info page to see what course code is being used
def test_quiz_info():
    with app.app_context():
        # Find a quiz that has submissions
        quiz = Quiz.query.get(7)  # PHYS101 quiz
        if not quiz:
            print("Quiz 7 not found")
            return
            
        course = Course.query.get(quiz.course_code)
        if not course:
            print(f"Course {quiz.course_code} not found")
            return
            
        # Find a student who has submissions for this quiz
        submissions = Submission.query.filter_by(quiz_id=quiz.id).all()
        if not submissions:
            print(f"No submissions found for quiz {quiz.id}")
            return
            
        student = User.query.get(submissions[0].user_id)
        if not student:
            print(f"Student {submissions[0].user_id} not found")
            return
            
        print(f"Testing quiz info for:")
        print(f"  Quiz: {quiz.name} (ID: {quiz.id})")
        print(f"  Course: {course.code}")
        print(f"  Student: {student.username}")
        print(f"  Expected URL: /course/{course.code}/quiz/{quiz.id}/results")
        
        # Check if the student is enrolled
        enrollment = CourseEnrollment.query.filter_by(
            student_id=student.id, 
            course_code=course.code
        ).first()
        
        if enrollment:
            print(f"  Student is enrolled: Yes")
        else:
            print(f"  Student is enrolled: No")

if __name__ == "__main__":
    test_quiz_info()