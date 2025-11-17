#!/usr/bin/env python
"""
Create test short answer data for demonstrating the results page
"""
from app import app, db
from models import ShortAnswer, Question, Submission, QuestionResponse, User
from datetime import datetime, timedelta
import random

def create_demo_data():
    with app.app_context():
        print("Creating demo short answer data...")
        
        # Get teacher user
        teacher = User.query.filter_by(role='teacher').first()
        if not teacher:
            print("No teacher found. Please create a teacher user first.")
            return None
        
        # Get students
        students = User.query.filter_by(role='student').limit(3).all()
        if len(students) < 2:
            print(f"Only {len(students)} student(s) found. Need at least 2 for demo.")
            return None
        
        # Create a short answer activity
        short_answer = ShortAnswer(
            course_code='PHYS101',
            name='Forces and Motion Quiz',
            description='Short answer questions about forces and motion concepts',
            created_by=teacher.id,
            duration=30,
            attempt_limit=2,
            point=100,
            point_in_course=10
        )
        db.session.add(short_answer)
        db.session.flush()
        print(f"Created Short Answer: {short_answer.name} (ID: {short_answer.id})")
        
        # Create questions
        questions_data = [
            {
                'content': 'Explain Newton\'s Second Law of Motion (F = ma)',
                'points': 35
            },
            {
                'content': 'Describe the difference between velocity and acceleration',
                'points': 30
            },
            {
                'content': 'What factors affect the force of friction?',
                'points': 35
            }
        ]
        
        questions = []
        for q_data in questions_data:
            q = Question(
                short_answer_id=short_answer.id,
                type='saq',
                content=q_data['content'],
                points=q_data['points']
            )
            db.session.add(q)
            questions.append(q)
        
        db.session.flush()
        print(f"Created {len(questions)} questions")
        
        # Create submissions from students
        sample_answers_by_student = {
            0: [  # First student
                'F = ma means force equals mass times acceleration. This shows that the acceleration of an object is directly proportional to the net force applied and inversely proportional to its mass.',
                'Velocity is the speed and direction of an object\'s motion (a vector). Acceleration is the rate of change of velocity over time. An object can have constant velocity but still accelerate if its direction changes.',
                'Friction depends on the normal force between surfaces, the types of materials in contact, and their surface roughness. Smoother surfaces typically have lower friction coefficients.'
            ],
            1: [  # Second student
                'Newton\'s Second Law states that F = ma. The force applied to an object equals its mass multiplied by the acceleration it produces. Heavier objects need more force to accelerate at the same rate as lighter objects.',
                'Velocity is how fast something moves in a particular direction. Acceleration measures how quickly the velocity changes. You can accelerate without changing speed if you change direction.',
                'The friction force depends on: 1) The weight of the object (normal force), 2) The surface texture of both objects, and 3) The type of surfaces (some materials create more friction than others).'
            ],
            2: [  # Third student
                'This law shows the relationship between force, mass, and acceleration. The greater the force, the greater the acceleration. The greater the mass, the less acceleration for the same force.',
                'Velocity tells us how fast and in what direction something moves. Acceleration tells us how quickly that velocity is changing. They are related but different concepts.',
                'Surface roughness, material properties, and the normal force between surfaces all affect friction. Different material combinations have different friction coefficients.'
            ]
        }
        
        total_points_possible = sum(q.points for q in questions)
        
        for student_idx, student in enumerate(students[:3]):
            submission = Submission(
                user_id=student.id,
                short_answer_id=short_answer.id,
                submitted_at=datetime.now() - timedelta(days=random.randint(0, 3)),
                total_score=random.randint(70, 98)
            )
            db.session.add(submission)
            db.session.flush()
            
            # Get student's answers
            answers = sample_answers_by_student.get(student_idx, sample_answers_by_student[0])
            
            # Create responses for each question
            for q_idx, question in enumerate(questions):
                points_earned = random.randint(int(question.points * 0.7), question.points)
                response = QuestionResponse(
                    submission_id=submission.id,
                    question_id=question.id,
                    text_answer=answers[q_idx] if q_idx < len(answers) else "No answer provided",
                    points=points_earned,
                    is_correct=(points_earned > question.points * 0.6)
                )
                db.session.add(response)
            
            print(f"Created submission from student: {student.username} (Score: {submission.total_score})")
        
        db.session.commit()
        
        print(f"\n✓ Demo data created successfully!")
        print(f"Access the results page at:")
        print(f"  /teacher/course/PHYS101/short-answer/{short_answer.id}/results")
        print(f"\nOr view it directly:")
        print(f"  http://127.0.0.1:5000/teacher/course/PHYS101/short-answer/{short_answer.id}/results")
        
        return short_answer.id

if __name__ == '__main__':
    sa_id = create_demo_data()
