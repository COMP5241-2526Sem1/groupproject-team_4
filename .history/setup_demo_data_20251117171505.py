#!/usr/bin/env python
"""
Create or verify short answer demo data
"""
from app import app, db
from models import ShortAnswer, Question, Submission, QuestionResponse, User, Course
from datetime import datetime, timedelta
import random

# Sample answers for realistic responses
SAMPLE_ANSWERS = {
    'Explain Newton\'s Second Law of Motion (F = ma)': [
        'F = ma means force equals mass times acceleration. This shows that the acceleration of an object is directly proportional to the net force applied and inversely proportional to its mass.',
        'Newton\'s Second Law states that F = ma. The force applied to an object equals its mass multiplied by the acceleration it produces. Heavier objects need more force to accelerate at the same rate as lighter objects.',
        'This law shows the relationship between force, mass, and acceleration. The greater the force, the greater the acceleration. The greater the mass, the less acceleration for the same force.',
        'The net force on an object is equal to the product of its mass and acceleration. If you double the force, the acceleration doubles. If you double the mass, the acceleration is halved.',
        'F = ma represents the fundamental principle that force causes acceleration. It tells us how much acceleration an object will experience when a force is applied.',
        'This is the most important law in classical mechanics, showing how objects respond to forces applied to them.',
    ],
    'Describe the difference between velocity and acceleration': [
        'Velocity is the speed and direction of an object\'s motion (a vector). Acceleration is the rate of change of velocity over time. An object can have constant velocity but still accelerate if its direction changes.',
        'Velocity tells us how fast and in what direction something moves. Acceleration tells us how quickly that velocity is changing. They are related but different concepts.',
        'Velocity is a vector quantity that describes motion in a particular direction. Acceleration is also a vector that describes how the velocity changes over time.',
        'An object moving at constant velocity has zero acceleration. Acceleration occurs whenever the velocity changes, including changes in speed or direction.',
        'Velocity is displacement per unit time, while acceleration is the change in velocity per unit time. You can be moving fast (high velocity) but have zero acceleration if your speed stays constant.',
        'A car driving at constant speed on a straight road has velocity but zero acceleration. A car speeding up or turning has both velocity and acceleration.',
    ],
    'What factors affect the force of friction?': [
        'Friction depends on the normal force between surfaces, the types of materials in contact, and their surface roughness. Smoother surfaces typically have lower friction coefficients.',
        'The friction force depends on: 1) The weight of the object (normal force), 2) The surface texture of both objects, and 3) The type of surfaces (some materials create more friction than others).',
        'Surface roughness, material properties, and the normal force between surfaces all affect friction. Different material combinations have different friction coefficients.',
        'Friction is affected by how hard the surfaces are pressed together (normal force) and how rough they are. Some material pairs naturally have more friction than others.',
        'The main factors are the normal force perpendicular to the surface and the coefficient of friction between the two materials. Smoother, harder surfaces generally have lower friction.',
        'Increasing the weight on an object increases friction. Also, different material pairs create different amounts of friction.',
    ]
}

def create_or_verify_data():
    with app.app_context():
        # Check if PHYS101 course exists
        course = Course.query.filter_by(code='PHYS101').first()
        if not course:
            print("❌ PHYS101 course not found!")
            return None
        
        # Check if short answer activity with ID 6 exists
        short_answer = ShortAnswer.query.filter_by(id=6).first()
        
        if short_answer:
            print(f"✓ Found existing short answer: {short_answer.name}")
            # Check if it already has submissions
            submissions = Submission.query.filter_by(short_answer_id=6).all()
            if submissions:
                print(f"✓ Already has {len(submissions)} submissions")
                return 6
            else:
                print("⚠ No submissions found, creating submissions...")
        else:
            print("⚠ Short answer ID 6 not found, creating new one...")
            
            # Get teacher
            teacher = User.query.filter_by(role='teacher').first()
            if not teacher:
                print("❌ No teacher found!")
                return None
            
            # Create short answer
            short_answer = ShortAnswer(
                id=6,
                course_code='PHYS101',
                name='Forces and Motion Quiz',
                description='Short answer questions about forces and motion concepts. Please provide detailed explanations for each question.',
                created_by=teacher.id,
                duration=30,
                attempt_limit=2,
                point=100,
                point_in_course=10
            )
            db.session.add(short_answer)
            db.session.flush()
            print(f"✓ Created short answer: {short_answer.name}")
            
            # Create questions
            questions_data = [
                {'content': 'Explain Newton\'s Second Law of Motion (F = ma)', 'points': 35},
                {'content': 'Describe the difference between velocity and acceleration', 'points': 30},
                {'content': 'What factors affect the force of friction?', 'points': 35}
            ]
            
            for q_data in questions_data:
                q = Question(
                    short_answer_id=short_answer.id,
                    type='saq',
                    content=q_data['content'],
                    points=q_data['points']
                )
                db.session.add(q)
            
            db.session.flush()
            print(f"✓ Created {len(questions_data)} questions")
        
        # Get questions
        questions = short_answer.questions
        
        # Get students
        students = User.query.filter_by(role='student').limit(5).all()
        
        if len(students) < 3:
            print(f"⚠ Only {len(students)} students found. Creating more...")
            for i in range(3 - len(students)):
                student = User(
                    username=f'student_demo_{i}',
                    password='password123',
                    role='student'
                )
                db.session.add(student)
            db.session.flush()
            students = User.query.filter_by(role='student').limit(5).all()
        
        # Create submissions
        num_students_to_add = min(5, len(students))
        existing_submissions = Submission.query.filter_by(short_answer_id=short_answer.id).all()
        
        if len(existing_submissions) < num_students_to_add:
            print(f"Creating submissions for {num_students_to_add} students...")
            
            for student_idx in range(num_students_to_add):
                student = students[student_idx]
                
                # Check if this student already has a submission
                existing = Submission.query.filter_by(
                    user_id=student.id,
                    short_answer_id=short_answer.id
                ).first()
                
                if existing:
                    continue
                
                submission = Submission(
                    user_id=student.id,
                    short_answer_id=short_answer.id,
                    submitted_at=datetime.now() - timedelta(days=random.randint(0, 3)),
                    total_score=random.randint(70, 98)
                )
                db.session.add(submission)
                db.session.flush()
                
                # Create responses for each question
                for question in questions:
                    sample_answers = SAMPLE_ANSWERS.get(question.content, ['Sample answer'])
                    text_answer = random.choice(sample_answers)
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
        
        print(f"\n✓ Demo data ready!")
        print(f"URL: http://127.0.0.1:5000/course/PHYS101/short-answer/6")
        
        return 6

if __name__ == '__main__':
    create_or_verify_data()
