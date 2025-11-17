#!/usr/bin/env python
"""Create sample short answer data"""
from app import app, db
from models import ShortAnswer, Question, Submission, QuestionResponse, User
from datetime import datetime

with app.app_context():
    # Check if short answer with ID 5 exists
    sa = ShortAnswer.query.get(5)
    
    if sa:
        print(f"Short Answer ID 5 already exists: '{sa.name}'")
    else:
        print("Creating Short Answer ID 5...")
        
        # Get a teacher
        teacher = User.query.filter_by(role='teacher').first()
        if not teacher:
            print("ERROR: No teacher found")
            exit(1)
        
        # Create short answer
        sa = ShortAnswer(
            id=5,  # Force ID=5
            course_code='PHYS101',
            name='Motion and Forces Quiz',
            description='Assess understanding of Newton\'s laws and motion concepts',
            created_by=teacher.id,
            duration=30,
            attempt_limit=2,
            point=100,
            point_in_course=10
        )
        db.session.add(sa)
        db.session.flush()
        
        # Create questions
        questions = [
            Question(
                short_answer_id=sa.id,
                type='saq',
                content='Explain Newton\'s Second Law of Motion',
                points=33
            ),
            Question(
                short_answer_id=sa.id,
                type='saq',
                content='What is the difference between speed and velocity?',
                points=33
            ),
            Question(
                short_answer_id=sa.id,
                type='saq',
                content='How does friction affect an object in motion?',
                points=34
            )
        ]
        
        for q in questions:
            db.session.add(q)
        
        db.session.commit()
        print(f"✓ Created Short Answer ID 5 with 3 questions")
        print(f"✓ Access at: http://127.0.0.1:5000/course/PHYS101/short-answer/5")
