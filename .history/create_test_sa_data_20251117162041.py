#!/usr/bin/env python
"""
Test script to create sample short answer data for testing the results page
"""
import sys
sys.path.insert(0, '/mnt/c/Users/Jennifer/Desktop/groupproject-team_4-DEV-ZHAO')

from app import app, db
from models import ShortAnswer, Question, Course, User, Submission, QuestionResponse
from datetime import datetime, timedelta
import random

def create_test_data():
    """Create test short answer data"""
    with app.app_context():
        print("Creating test short answer data...")
        
        # Get or create course
        course = Course.query.filter_by(code='PHYS101').first()
        if not course:
            print("PHYS101 course not found. Creating it...")
            # Find a teacher
            teacher = User.query.filter_by(role='teacher').first()
            if not teacher:
                print("No teacher found in database")
                return
            
            course = Course(
                code='PHYS101',
                name='Physics 101',
                description='Introduction to Physics',
                teacher_id=teacher.id
            )
            db.session.add(course)
            db.session.flush()
        
        # Create a new short answer activity
        short_answer = ShortAnswer(
            course_code=course.code,
            name='Test Short Answer Activity',
            description='This is a test short answer activity for testing the results page',
            created_by=course.teacher_id,
            duration=20,
            attempt_limit=3,
            point=100,
            point_in_course=5
        )
        db.session.add(short_answer)
        db.session.flush()
        
        # Create questions
        questions_data = [
            {'content': 'Explain Newton\'s first law of motion', 'points': 30},
            {'content': 'Describe the concept of acceleration', 'points': 35},
            {'content': 'What is the relationship between force and mass?', 'points': 35}
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
        
        # Create sample student submissions and responses
        students = User.query.filter_by(role='student').limit(3).all()
        
        if not students:
            print("No students found in database. Creating test students...")
            for i in range(1, 4):
                student = User(
                    username=f'teststudent{i}',
                    password=f'password{i}',
                    role='student'
                )
                db.session.add(student)
            db.session.flush()
            students = User.query.filter_by(role='student').limit(3).all()
        
        # Create submissions for each student
        sample_answers = [
            [
                'Newton\'s first law states that an object at rest remains at rest and an object in motion remains in motion unless acted upon by a force.',
                'Acceleration is the rate of change of velocity over time. It can be positive (speeding up) or negative (slowing down).',
                'The relationship is given by F = ma, where force equals mass times acceleration.'
            ],
            [
                'Objects tend to maintain their state of motion. Without external forces, there is no change in motion.',
                'Acceleration describes how quickly an object\'s velocity changes. It is a vector quantity with both magnitude and direction.',
                'Force is proportional to mass and acceleration (F = ma). Greater mass requires more force to produce same acceleration.'
            ],
            [
                'An object will not accelerate unless a net force is applied to it. This is the foundation of classical mechanics.',
                'The rate at which velocity changes is acceleration. It can occur due to changes in speed or direction.',
                'The fundamental equation F = ma shows that force and mass are directly related to acceleration.'
            ]
        ]
        
        for student_idx, student in enumerate(students):
            submission = Submission(
                user_id=student.id,
                short_answer_id=short_answer.id,
                submitted_at=datetime.now() - timedelta(days=random.randint(1, 5)),
                total_score=random.randint(70, 95)
            )
            db.session.add(submission)
            db.session.flush()
            
            # Create responses for each question
            for q_idx, question in enumerate(questions):
                response = QuestionResponse(
                    submission_id=submission.id,
                    question_id=question.id,
                    text_answer=sample_answers[student_idx][q_idx],
                    points=random.randint(20, question.points),
                    is_correct=True
                )
                db.session.add(response)
        
        db.session.commit()
        print(f"✓ Test data created successfully!")
        print(f"  - Short Answer: '{short_answer.name}' (ID: {short_answer.id})")
        print(f"  - Questions: {len(questions)}")
        print(f"  - Submissions: {len(students)}")
        print(f"  - Course: {course.code}")
        return short_answer.id, course.code

if __name__ == '__main__':
    sa_id, course_code = create_test_data()
    print(f"\nAccess results page at: /teacher/course/{course_code}/short-answer/{sa_id}/results")
