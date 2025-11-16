from app import app
from models import db, Quiz, User, Attempt, Submission

with app.app_context():
    # Check alice_johnson's current attempts for quiz 4
    alice = User.query.filter_by(username='alice_johnson').first()
    quiz = Quiz.query.filter_by(id=4).first()
    
    if alice and quiz:
        attempts = Attempt.query.filter_by(quiz_id=4, user_id=alice.id).count()
        submissions = Submission.query.filter_by(quiz_id=4, user_id=alice.id).count()
        
        print(f"Alice Johnson (ID: {alice.id})")
        print(f"Quiz 4 (COMP101): {quiz.name}")
        print(f"Attempt limit: {quiz.attempt_limit}")
        print(f"Current attempts: {attempts}")
        print(f"Current submissions: {submissions}")
        print(f"Can attempt: {attempts < quiz.attempt_limit}")
        
        # Check if we can find a quiz where alice has used all attempts
        print("\nChecking all quizzes for alice:")
        all_quizzes = Quiz.query.join(Course).filter(Course.course_code == 'COMP101').all()
        for q in all_quizzes:
            attempts = Attempt.query.filter_by(quiz_id=q.id, user_id=alice.id).count()
            can_attempt = attempts < (q.attempt_limit or 999)
            print(f"  Quiz {q.id}: {q.name} - Attempts: {attempts}/{q.attempt_limit} - Can attempt: {can_attempt}")