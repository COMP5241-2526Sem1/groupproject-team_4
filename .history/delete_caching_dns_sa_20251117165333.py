#!/usr/bin/env python
"""Find and delete the specific short answer activity"""
from app import app, db
from models import ShortAnswer, Question, Submission, QuestionResponse

with app.app_context():
    print("=== Searching for Short Answer Activity ===\n")
    
    # Search patterns to find the activity
    search_terms = [
        'Caching DNS Information - Critical Thinking Questions',
        'Caching DNS Information',
        'DNS'
    ]
    
    sa = None
    for term in search_terms:
        sa = ShortAnswer.query.filter(ShortAnswer.name.ilike(f'%{term}%')).first()
        if sa:
            print(f"Found using search term: '{term}'")
            break
    
    if sa:
        print(f"\nShort Answer Activity Details:")
        print(f"  ID: {sa.id}")
        print(f"  Name: '{sa.name}'")
        print(f"  Course: {sa.course_code}")
        print(f"  Questions: {len(sa.questions)}")
        print(f"  Submissions: {len(sa.submissions)}")
        
        # Check for related data
        questions = Question.query.filter_by(short_answer_id=sa.id).all()
        submissions = Submission.query.filter_by(short_answer_id=sa.id).all()
        
        print(f"\nCascading Deletion:")
        
        # Delete all submissions first
        response_count = 0
        if submissions:
            for sub in submissions:
                # Delete question responses
                responses = QuestionResponse.query.filter_by(submission_id=sub.id).all()
                response_count += len(responses)
                for resp in responses:
                    db.session.delete(resp)
                # Delete submission
                db.session.delete(sub)
            print(f"  ✓ Deleted {len(submissions)} submission(s)")
            print(f"  ✓ Deleted {response_count} response(s)")
        
        # Delete all questions
        if questions:
            for q in questions:
                db.session.delete(q)
            print(f"  ✓ Deleted {len(questions)} question(s)")
        
        # Delete the short answer activity
        db.session.delete(sa)
        db.session.commit()
        print(f"  ✓ Deleted short answer activity")
        print(f"\n✓✓✓ Successfully deleted: '{sa.name}'")
        
    else:
        print("Short answer not found. Checking all activities in PHYS101...\n")
        sas = ShortAnswer.query.filter_by(course_code='PHYS101').all()
        print(f"Found {len(sas)} short answer activities in PHYS101:")
        for s in sas:
            print(f"  - ID {s.id}: '{s.name}'")
