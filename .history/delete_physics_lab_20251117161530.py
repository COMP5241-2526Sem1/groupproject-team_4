from app import app
from models.short_answer import ShortAnswer
from models.question import Question
from models.question_response import QuestionResponse
from models.submission import Submission
from database import db

with app.app_context():
    # Find Physics Lab Report short answer
    short_answer = ShortAnswer.query.filter_by(
        course_code='PHYS101',
        name='Physics Lab Report'
    ).first()
    
    if short_answer:
        print(f"Found: Short Answer ID={short_answer.id}, Name='{short_answer.name}'")
        
        # Get related data
        questions = Question.query.filter_by(short_answer_id=short_answer.id).all()
        submissions = Submission.query.filter_by(short_answer_id=short_answer.id).all()
        responses = QuestionResponse.query.join(Question).filter(
            Question.short_answer_id == short_answer.id
        ).all()
        
        print(f"Questions: {len(questions)}")
        print(f"Submissions: {len(submissions)}")
        print(f"Question Responses: {len(responses)}")
        
        print("\n--- Deleting Physics Lab Report ---")
        
        # Delete in correct order
        # 1. Delete question responses
        for resp in responses:
            db.session.delete(resp)
        print(f"Deleted {len(responses)} question responses")
        
        # 2. Delete submissions
        for sub in submissions:
            db.session.delete(sub)
        print(f"Deleted {len(submissions)} submissions")
        
        # 3. Delete questions
        for q in questions:
            db.session.delete(q)
        print(f"Deleted {len(questions)} questions")
        
        # 4. Delete short answer
        db.session.delete(short_answer)
        print(f"Deleted short answer")
        
        db.session.commit()
        print("\n✓ Physics Lab Report deleted successfully!")
    else:
        print("Physics Lab Report not found")
