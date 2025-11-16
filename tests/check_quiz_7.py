from app import app
from models import db, User, Course, Quiz, CourseEnrollment, Submission

with app.app_context():
    # Check the specific quiz mentioned in the error (quiz ID 7)
    quiz = Quiz.query.get(7)
    if quiz:
        course = Course.query.get(quiz.course_code)
        print(f'Quiz ID 7: {quiz.name}, Course: {course.code if course else "None"}, Course Code: {quiz.course_code}')
        
        # Check all quizzes to see their course codes
        print('\nAll quizzes:')
        all_quizzes = Quiz.query.all()
        for q in all_quizzes:
            print(f'Quiz ID {q.id}: {q.name}, Course Code: {q.course_code}')
    else:
        print('Quiz ID 7 not found')
        
    # Check if there are any quizzes with empty course codes
    print('\nChecking for empty course codes:')
    empty_course_quizzes = Quiz.query.filter(Quiz.course_code == '').all()
    if empty_course_quizzes:
        print(f'Found {len(empty_course_quizzes)} quizzes with empty course codes')
        for q in empty_course_quizzes:
            print(f'Quiz ID {q.id}: {q.name}')
    else:
        print('No quizzes with empty course codes found')