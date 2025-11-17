from app import app
from models.poll import Poll
from models.question import Question
from models.question_response import QuestionResponse
from models.submission import Submission
from database import db

with app.app_context():
    # Find poll with id=5
    poll = Poll.query.get(5)
    
    if poll:
        print(f"Poll ID: {poll.id}")
        print(f"Poll Name: {poll.name}")
        print(f"Course: {poll.course_code}")
        
        # Get related data
        questions = Question.query.filter_by(poll_id=5).all()
        submissions = Submission.query.filter_by(poll_id=5).all()
        responses = QuestionResponse.query.join(Question).filter(Question.poll_id == 5).all()
        
        print(f"\nQuestions: {len(questions)}")
        print(f"Submissions: {len(submissions)}")
        print(f"Question Responses: {len(responses)}")
        
        print("\n--- Deleting poll_id=5 ---")
        
        # Delete in correct order (respecting foreign key constraints)
        # 1. Delete question responses
        for resp in responses:
            db.session.delete(resp)
        print(f"Deleted {len(responses)} question responses")
        
        # 2. Delete submissions
        for sub in submissions:
            db.session.delete(sub)
        print(f"Deleted {len(submissions)} submissions")
        
        # 3. Delete questions (will cascade delete choices)
        for q in questions:
            db.session.delete(q)
        print(f"Deleted {len(questions)} questions")
        
        # 4. Delete poll
        db.session.delete(poll)
        print(f"Deleted poll ID=5")
        
        db.session.commit()
        print("\n✓ All related data deleted successfully!")
    else:
        print("Poll with ID=5 not found")
