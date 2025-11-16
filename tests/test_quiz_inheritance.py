#!/usr/bin/env python3
"""
Test script to demonstrate Quiz inheritance from Task and accessing name property
"""

from app import app
from database import init_db, db
from models.quiz import Quiz


def test_quiz_direct_model():
    """Test that Quiz can access its properties directly (no inheritance)"""
    
    with app.app_context():
        # Initialize the database
        init_db()
        
        print("=== Testing Direct Quiz Model (No Task Inheritance) ===\n")
        
        # Query a quiz and show how to access its properties directly
        quiz = db.session.query(Quiz).first()
        if quiz:
            print(f'✓ Quiz ID: {quiz.id}')
            print(f'✓ Quiz name (direct property): {quiz.name}')
            print(f'✓ Quiz description: {quiz.description}')
            print(f'✓ Course Code: {quiz.course_code}')
            print(f'✓ Created by: {quiz.created_by}')
            print(f'✓ Duration: {quiz.duration} minutes')
            print(f'✓ Points: {quiz.point}')
            print(f'✓ Quiz-specific visibility settings:')
            print(f'  - Question visible after submission: {quiz.after_submitted_question_visible}')
            print(f'  - Student response visible: {quiz.after_submitted_student_response_visible}')
            print(f'  - Sample response visible: {quiz.after_submitted_sample_response_visible}')
            print(f'  - Class response visible: {quiz.after_submitted_class_response_visible}')
        else:
            print('⚠ No quiz found in database')
        
        print("\n=== SQL Query Example (No JOIN needed) ===")
        # Show how to query using SQL directly (no task table join)
        from sqlalchemy import text
        result = db.session.execute(text('''
            SELECT q.id, q.name, q.description, q.after_submitted_question_visible 
            FROM quiz q 
            LIMIT 1
        ''')).fetchone()
        
        if result:
            print(f'SQL Result:')
            print(f'  - Quiz ID: {result[0]}')
            print(f'  - Name: {result[1]}')
            print(f'  - Description: {result[2]}')
            print(f'  - Question visible after submission: {result[3]}')
        
        print("\n=== All Quizzes with Names ===")
        # Show all quizzes with their names
        all_quizzes = db.session.query(Quiz).all()
        for quiz in all_quizzes:
            print(f"Quiz ID {quiz.id}: '{quiz.name}'")

if __name__ == "__main__":
    test_quiz_direct_model()