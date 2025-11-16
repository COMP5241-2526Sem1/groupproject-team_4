from database import db
from models.user import User
from models.quiz import Quiz
from models.submission import Submission
from models.attempt import Attempt
from flask import Flask
from app import app

def find_completed_quizzes():
    """Find users who have completed all attempts for quizzes"""
    
    with app.app_context():
        # Get all quizzes with attempt limits
        quizzes = Quiz.query.filter(Quiz.attempt_limit.isnot(None)).all()
        
        for quiz in quizzes:
            print(f"\n=== Quiz: {quiz.name} (ID: {quiz.id}) ===")
            print(f"Attempt Limit: {quiz.attempt_limit}")
            
            # Get all submissions for this quiz
            submissions = Submission.query.filter_by(quiz_id=quiz.id).all()
            
            # Group by user
            user_submissions = {}
            for sub in submissions:
                if sub.user_id not in user_submissions:
                    user_submissions[sub.user_id] = []
                user_submissions[sub.user_id].append(sub)
            
            # Check each user
            for user_id, user_subs in user_submissions.items():
                user = User.query.get(user_id)
                attempt_count = Attempt.query.filter_by(quiz_id=quiz.id, user_id=user_id).count()
                
                print(f"\nUser {user.username} (ID: {user_id}):")
                print(f"  Attempts Used: {attempt_count}")
                print(f"  Submissions: {len(user_subs)}")
                print(f"  Can Attempt: {attempt_count < quiz.attempt_limit}")
                
                if attempt_count >= quiz.attempt_limit:
                    print(f"  ✅ COMPLETED - All attempts used!")
                    if user_subs:
                        latest_sub = max(user_subs, key=lambda x: x.submitted_at)
                        print(f"  Latest Grade: {latest_sub.grade}")
                        print(f"  Latest Date: {latest_sub.submitted_at}")
                else:
                    print(f"  ❌ Not completed - {quiz.attempt_limit - attempt_count} attempts remaining")

if __name__ == "__main__":
    find_completed_quizzes()