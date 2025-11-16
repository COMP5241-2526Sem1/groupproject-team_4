from app import app
from models import db, Quiz, User, Attempt, Submission, Course

with app.app_context():
    # Find users who have used all attempts for any quiz
    print("Searching for users who have used all attempts...")
    
    # Get all quizzes
    all_quizzes = Quiz.query.all()
    
    for quiz in all_quizzes:
        if quiz.attempt_limit:  # Only check quizzes with attempt limits
            # Get all users who have attempts for this quiz
            user_attempts = db.session.query(
                Attempt.user_id,
                db.func.count(Attempt.id).label('attempt_count')
            ).filter_by(quiz_id=quiz.id).group_by(Attempt.user_id).all()
            
            for user_id, attempt_count in user_attempts:
                if attempt_count >= quiz.attempt_limit:
                    user = User.query.get(user_id)
                    if user:
                        print(f"🎯 Found user who used all attempts!")
                        print(f"  User: {user.username} ({user.role})")
                        print(f"  Quiz {quiz.id}: {quiz.name}")
                        print(f"  Attempts: {attempt_count}/{quiz.attempt_limit}")
                        print(f"  Course: {quiz.course_code}")
                        print()
                        
                        # Test this scenario
                        print(f"Testing quiz info page for {user.username} on quiz {quiz.id}...")
                        # This would be a good test case for the View Results button issue