#!/usr/bin/env python
"""Find and delete the specific short answer activity"""
from app import app, db
from models import ShortAnswer, Question, Submission, QuestionResponse

with app.app_context():
    print("Looking for 'Caching DNS Information - Critical Thinking Questions'...\n")
    
    # Find the short answer by name
    sa = ShortAnswer.query.filter_by(
        course_code='PHYS101',
        name='Caching DNS Information - Critical Thinking Questions'
    ).first()
    
    if sa:
        print(f"Found: ID={sa.id}, Name='{sa.name}'")
        print(f"Questions: {len(sa.questions)}")
        print(f"Submissions: {len(sa.submissions)}")
        
        # Check for related data
        questions = Question.query.filter_by(short_answer_id=sa.id).all()
        submissions = Submission.query.filter_by(short_answer_id=sa.id).all()
        
        print(f"\nRelated Questions: {len(questions)}")
        print(f"Related Submissions: {len(submissions)}")
        
        # Delete all submissions first
        if submissions:
            for sub in submissions:
                # Delete question responses
                responses = QuestionResponse.query.filter_by(submission_id=sub.id).all()
                for resp in responses:
                    db.session.delete(resp)
                # Delete submission
                db.session.delete(sub)
            print(f"✓ Deleted {len(submissions)} submissions and their responses")
        
        # Delete all questions
        if questions:
            for q in questions:
                db.session.delete(q)
            print(f"✓ Deleted {len(questions)} questions")
        
        # Delete the short answer activity
        db.session.delete(sa)
        db.session.commit()
        print(f"\n✓ Deleted short answer activity: '{sa.name}'")
        
    else:
        print("Short answer not found. Checking all activities in PHYS101...\n")
        sas = ShortAnswer.query.filter_by(course_code='PHYS101').all()
        print(f"Found {len(sas)} short answer activities in PHYS101:")
        for s in sas:
            print(f"  - ID {s.id}: '{s.name}'")
