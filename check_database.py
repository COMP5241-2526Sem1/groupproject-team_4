from app import app
from models import db, User, Course, Quiz, CourseEnrollment, Submission

with app.app_context():
    # Check if we have any quiz submissions
    submissions = Submission.query.all()
    print(f'Total submissions: {len(submissions)}')
    
    if submissions:
        for sub in submissions[:3]:  # Check first 3
            user = User.query.get(sub.user_id)
            quiz = Quiz.query.get(sub.quiz_id)
            if quiz:
                course = Course.query.get(quiz.course_code)
                print(f'Submission: User={user.username if user else "Unknown"}, Quiz={quiz.name}, Course={course.code if course else "Unknown"}')
            else:
                print(f'Submission: User={user.username if user else "Unknown"}, Quiz ID={sub.quiz_id} (not found)')
    
    # Check courses and quizzes
    courses = Course.query.all()
    print(f'\nTotal courses: {len(courses)}')
    for course in courses[:3]:
        quizzes = Quiz.query.filter_by(course_code=course.code).all()
        print(f'Course {course.code}: {len(quizzes)} quizzes')