#!/usr/bin/env python
"""Check short answer data in database"""
from app import app, db
from models import ShortAnswer

with app.app_context():
    short_answers = ShortAnswer.query.all()
    print(f"Total Short Answer activities: {len(short_answers)}")
    for sa in short_answers:
        print(f"  - ID: {sa.id}, Name: '{sa.name}', Course: {sa.course_code}, Questions: {len(sa.questions)}, Submissions: {len(sa.submissions)}")
    
    if not short_answers:
        print("\nNo short answer activities found. Creating sample data...")
        from models import User, Question, Submission, QuestionResponse
        from datetime import datetime, timedelta
        import random
        
        # Get teacher
        teacher = User.query.filter_by(role='teacher').first()
        if not teacher:
            print("No teacher found")
        else:
            # Get students
            students = User.query.filter_by(role='student').limit(3).all()
            if len(students) < 1:
                print("Not enough students")
            else:
                # Create short answer
                sa = ShortAnswer(
                    course_code='PHYS101',
                    name='Force and Motion Assessment',
                    description='Questions about Newton\'s laws and motion concepts',
                    created_by=teacher.id,
                    duration=30,
                    attempt_limit=2,
                    point=100,
                    point_in_course=10
                )
                db.session.add(sa)
                db.session.flush()
                
                # Create questions
                q1 = Question(
                    short_answer_id=sa.id,
                    type='saq',
                    content='Explain Newton\'s Second Law (F = ma)',
                    points=33
                )
                q2 = Question(
                    short_answer_id=sa.id,
                    type='saq',
                    content='What is the difference between velocity and acceleration?',
                    points=33
                )
                q3 = Question(
                    short_answer_id=sa.id,
                    type='saq',
                    content='Describe how friction affects motion',
                    points=34
                )
                db.session.add(q1)
                db.session.add(q2)
                db.session.add(q3)
                db.session.flush()
                
                # Create submission from first student
                sub = Submission(
                    user_id=students[0].id,
                    short_answer_id=sa.id,
                    submitted_at=datetime.now() - timedelta(days=1),
                    total_score=85
                )
                db.session.add(sub)
                db.session.flush()
                
                # Create responses
                r1 = QuestionResponse(
                    submission_id=sub.id,
                    question_id=q1.id,
                    text_answer='Newton\'s Second Law states that the force acting on an object is equal to the mass of that object times its acceleration.',
                    points=30,
                    is_correct=True
                )
                r2 = QuestionResponse(
                    submission_id=sub.id,
                    question_id=q2.id,
                    text_answer='Velocity is the speed and direction of motion, while acceleration is how quickly velocity changes.',
                    points=28,
                    is_correct=True
                )
                r3 = QuestionResponse(
                    submission_id=sub.id,
                    question_id=q3.id,
                    text_answer='Friction is a force that opposes motion between surfaces in contact.',
                    points=27,
                    is_correct=True
                )
                db.session.add(r1)
                db.session.add(r2)
                db.session.add(r3)
                
                db.session.commit()
                print(f"✓ Created sample short answer (ID: {sa.id})")
                print(f"  URL: /course/PHYS101/short-answer/{sa.id}")
