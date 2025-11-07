# Check all quizzes and attempts for carol_davis
from models import User, Quiz, Attempt
from database import db
from app import app

with app.app_context():
    # Find carol_davis
    user = User.query.filter_by(username='carol_davis').first()
    if not user:
        print("User not found")
        exit(1)
    
    print(f"User: {user.username} (ID: {user.id}, Role: {user.role})")
    
    # Find all attempts by this user
    attempts = Attempt.query.filter_by(user_id=user.id).all()
    print(f"Total attempts: {len(attempts)}")
    
    for attempt in attempts:
        quiz = Quiz.query.get(attempt.quiz_id)
        if quiz:
            print(f"  Attempt {attempt.id}: Quiz {quiz.id} - {quiz.name} (Course: {quiz.course_code}) - Attempt #{attempt.attempt_count}")
    
    # Find all quizzes
    all_quizzes = Quiz.query.all()
    print(f"\nAll quizzes in database: {len(all_quizzes)}")
    for quiz in all_quizzes:
        attempts_count = Attempt.query.filter_by(user_id=user.id, quiz_id=quiz.id).count()
        print(f"  Quiz {quiz.id}: {quiz.name} (Course: {quiz.course_code}) - User attempts: {attempts_count}")