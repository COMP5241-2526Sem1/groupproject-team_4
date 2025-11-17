#!/usr/bin/env python
"""
Create demo student answers for short answer activity ID 6
"""
from app import app, db
from models import ShortAnswer, Question, Submission, QuestionResponse, User
from datetime import datetime, timedelta
import random

# Sample answers for realistic responses
SAMPLE_ANSWERS = {
    0: [  # Q1 answers
        'F = ma means force equals mass times acceleration. This shows that the acceleration of an object is directly proportional to the net force applied and inversely proportional to its mass.',
        'Newton\'s Second Law states that F = ma. The force applied to an object equals its mass multiplied by the acceleration it produces. Heavier objects need more force to accelerate at the same rate as lighter objects.',
        'This law shows the relationship between force, mass, and acceleration. The greater the force, the greater the acceleration. The greater the mass, the less acceleration for the same force.',
        'The net force on an object is equal to the product of its mass and acceleration. If you double the force, the acceleration doubles. If you double the mass, the acceleration is halved.',
        'F = ma represents the fundamental principle that force causes acceleration. It tells us how much acceleration an object will experience when a force is applied.',
    ],
    1: [  # Q2 answers
        'Velocity is the speed and direction of an object\'s motion (a vector). Acceleration is the rate of change of velocity over time. An object can have constant velocity but still accelerate if its direction changes.',
        'Velocity tells us how fast and in what direction something moves. Acceleration tells us how quickly that velocity is changing. They are related but different concepts.',
        'Velocity is a vector quantity that describes motion in a particular direction. Acceleration is also a vector that describes how the velocity changes over time.',
        'An object moving at constant velocity has zero acceleration. Acceleration occurs whenever the velocity changes, including changes in speed or direction.',
        'Velocity is displacement per unit time, while acceleration is the change in velocity per unit time. You can be moving fast (high velocity) but have zero acceleration if your speed stays constant.',
    ],
    2: [  # Q3 answers
        'Friction depends on the normal force between surfaces, the types of materials in contact, and their surface roughness. Smoother surfaces typically have lower friction coefficients.',
        'The friction force depends on: 1) The weight of the object (normal force), 2) The surface texture of both objects, and 3) The type of surfaces (some materials create more friction than others).',
        'Surface roughness, material properties, and the normal force between surfaces all affect friction. Different material combinations have different friction coefficients.',
        'Friction is affected by how hard the surfaces are pressed together (normal force) and how rough they are. Some material pairs naturally have more friction than others.',
        'The main factors are the normal force perpendicular to the surface and the coefficient of friction between the two materials. Smoother, harder surfaces generally have lower friction.',
    ]
}

def create_demo_answers():
    with app.app_context():
        # Get short answer with ID 6
        short_answer = ShortAnswer.query.filter_by(id=6).first()
        
        if not short_answer:
            print("❌ Short answer ID 6 not found!")
            return
        
        print(f"✓ Found short answer: {short_answer.name}")
        
        # Get questions
        questions = short_answer.questions
        if not questions:
            print("❌ No questions found!")
            return
        
        print(f"✓ Found {len(questions)} questions")
        
        # Get students
        students = User.query.filter_by(role='student').all()
        print(f"✓ Found {len(students)} students")
        
        if len(students) < 5:
            # Create more test students
            for i in range(5 - len(students)):
                student = User(
                    username=f'student_test_{i}',
                    password='password123',
                    role='student'
                )
                db.session.add(student)
            db.session.flush()
            students = User.query.filter_by(role='student').all()
            print(f"✓ Created additional students, total now: {len(students)}")
        
        # Delete existing submissions for clean demo
        existing_subs = Submission.query.filter_by(short_answer_id=6).all()
        for sub in existing_subs:
            db.session.delete(sub)
        db.session.commit()
        print(f"✓ Cleared {len(existing_subs)} existing submissions")
        
        # Create new submissions
        for student_idx in range(5):
            student = students[student_idx]
            
            # Create submission
            submission = Submission(
                user_id=student.id,
                short_answer_id=short_answer.id,
                submitted_at=datetime.now() - timedelta(days=random.randint(0, 3), hours=random.randint(0, 23)),
                total_score=random.randint(70, 98)
            )
            db.session.add(submission)
            db.session.flush()
            
            # Create responses for each question
            for q_idx, question in enumerate(questions):
                answer_options = SAMPLE_ANSWERS.get(q_idx, ['Sample answer'])
                text_answer = random.choice(answer_options)
                points_earned = random.randint(int(question.points * 0.7), question.points)
                
                response = QuestionResponse(
                    submission_id=submission.id,
                    question_id=question.id,
                    text_answer=text_answer,
                    points=points_earned,
                    is_correct=(points_earned > question.points * 0.6)
                )
                db.session.add(response)
            
            db.session.flush()
            print(f"  ✓ Created submission for {student.username}")
        
        db.session.commit()
        print(f"\n✅ Demo data created successfully!")
        print(f"   Visit: http://127.0.0.1:5000/course/PHYS101/short-answer/6")

if __name__ == '__main__':
    create_demo_answers()
