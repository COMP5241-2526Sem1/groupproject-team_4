from app import app
from models import db, Quiz, User, Attempt, Submission, Course

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
        all_quizzes = Quiz.query.join(Course).filter(Course.code == 'COMP101').all()
        for q in all_quizzes:
            attempts = Attempt.query.filter_by(quiz_id=q.id, user_id=alice.id).count()
            can_attempt = attempts < (q.attempt_limit or 999)
            print(f"  Quiz {q.id}: {q.name} - Attempts: {attempts}/{q.attempt_limit} - Can attempt: {can_attempt}")
            
            # If we find a quiz where alice can't attempt anymore, let's test it
            if not can_attempt and attempts > 0:
                print(f"\n🎯 Found quiz where alice can't attempt anymore: Quiz {q.id}")
                break
                
        # Let's also check what happens when we manually set alice to have 3 attempts
        print(f"\n🧪 Simulating alice using all 3 attempts on quiz 4:")
        print(f"If alice had 3 attempts: can_attempt = {3 < quiz.attempt_limit}")
        print(f"This would show 'View Results' button instead of 'Start Quiz'")