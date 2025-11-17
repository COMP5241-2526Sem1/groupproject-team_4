#!/usr/bin/env python
"""Verify short answer data in database"""
from app import app, db
from models import ShortAnswer, Question, Submission, QuestionResponse, User

with app.app_context():
    print("=== Short Answer Data Verification ===\n")
    
    # Check short answers
    sas = ShortAnswer.query.all()
    print(f"Total Short Answer activities: {len(sas)}")
    
    for sa in sas:
        print(f"\n📋 ID {sa.id}: '{sa.name}'")
        print(f"   Course: {sa.course_code}")
        print(f"   Questions: {len(sa.questions)}")
        print(f"   Submissions: {len(sa.submissions)}")
        
        if sa.id == 1:
            print(f"   ✓ Access URL: http://127.0.0.1:5000/course/{sa.course_code}/short-answer/{sa.id}")
    
    print("\n=== Testing Template Rendering ===\n")
    
    # Get the first short answer for testing
    sa = ShortAnswer.query.first()
    if sa:
        course = sa.course
        print(f"Course object: {course}")
        print(f"Course code: {course.code if course else 'N/A'}")
        print(f"Short Answer: {sa.name}")
        print(f"Questions: {[q.content for q in sa.questions]}")
        
        # Get a user for testing
        user = User.query.filter_by(role='student').first()
        if user:
            submissions = Submission.query.filter_by(
                user_id=user.id,
                short_answer_id=sa.id
            ).all()
            print(f"Student submissions: {len(submissions)}")
