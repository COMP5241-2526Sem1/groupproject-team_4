#!/usr/bin/env python
"""
Quick script to create test short answer data in database
Run this to populate the database with sample short answer activities
"""
from app import app, db
from models import ShortAnswer, Question, User

def create_test_data():
    with app.app_context():
        print("Checking existing short answer activities...")
        
        existing = ShortAnswer.query.all()
        print(f"Found {len(existing)} existing short answer activities")
        
        # Get a teacher
        teacher = User.query.filter_by(role='teacher').first()
        if not teacher:
            print("ERROR: No teacher user found in database!")
            print("Please create a teacher user first.")
            return False
        
        print(f"Using teacher: {teacher.username}")
        
        # Create sample short answer if none exist
        if len(existing) == 0:
            print("\nCreating sample short answer activities...")
            
            # Activity 1
            sa1 = ShortAnswer(
                course_code='PHYS101',
                name='Motion and Forces Quiz',
                description='Assess your understanding of Newton\'s laws and motion concepts',
                created_by=teacher.id,
                duration=30,
                attempt_limit=2,
                point=100,
                point_in_course=10
            )
            db.session.add(sa1)
            db.session.flush()
            
            # Add questions to activity 1
            q1 = Question(
                short_answer_id=sa1.id,
                type='saq',
                content='Explain Newton\'s Second Law of Motion (F = ma)',
                points=33
            )
            q2 = Question(
                short_answer_id=sa1.id,
                type='saq',
                content='What is the difference between speed and velocity?',
                points=33
            )
            q3 = Question(
                short_answer_id=sa1.id,
                type='saq',
                content='How does friction affect motion?',
                points=34
            )
            db.session.add_all([q1, q2, q3])
            
            db.session.commit()
            print(f"✓ Created 'Motion and Forces Quiz' (ID: {sa1.id})")
            print(f"  Access at: http://127.0.0.1:5000/teacher/course/PHYS101/short-answer")
            print(f"  View details: http://127.0.0.1:5000/course/PHYS101/short-answer/{sa1.id}")
            
        else:
            print(f"\n✓ Database already has {len(existing)} short answer activit(ies)")
            print("\nExisting activities:")
            for sa in existing:
                print(f"  - ID {sa.id}: '{sa.name}' ({len(sa.questions)} questions)")
                print(f"    Access: http://127.0.0.1:5000/course/{sa.course_code}/short-answer/{sa.id}")
        
        return True

if __name__ == '__main__':
    if create_test_data():
        print("\n✓ Setup complete!")
    else:
        print("\n✗ Setup failed")
