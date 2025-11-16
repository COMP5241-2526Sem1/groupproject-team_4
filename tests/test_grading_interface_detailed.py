#!/usr/bin/env python3

from flask import Flask
from flask.testing import FlaskClient
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import db
from models.user import User
from models.course import Course
from models.course_enrollment import CourseEnrollment
from models.quiz import Quiz
from models.question import Question
from models.submission import Submission
from models.question_response import QuestionResponse

def test_grading_interface_detailed():
    """Test the teacher grading interface with detailed output"""
    
    with app.app_context():
        # Create test client
        with app.test_client() as client:
            # Login as teacher
            with client.session_transaction() as sess:
                sess['user_id'] = 30  # Teacher ID
            
            # Test the grading interface
            response = client.get('/teacher/course/PHYS101/quiz/13/grading')
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Length: {len(response.data)}")
            
            if response.status_code == 200:
                html_content = response.data.decode('utf-8')
                
                print("\n--- Checking for student data ---")
                # Check what student data is available
                students = User.query.filter(User.id.in_([34, 36])).all()
                for student in students:
                    print(f"Student ID: {student.id}, Username: {student.username}")
                    if student.username in html_content:
                        print(f"✓ Found student: {student.username}")
                    else:
                        print(f"✗ Missing student: {student.username}")
                
                print("\n--- Checking for question content ---")
                # Check what question content is available
                saq_questions = Question.query.filter_by(quiz_id=13, type='saq').all()
                for question in saq_questions:
                    print(f"Question ID: {question.id}, Content: {question.content}")
                    if question.content in html_content:
                        print(f"✓ Found question content")
                    else:
                        print(f"✗ Missing question content")
                
                print("\n--- HTML Sample ---")
                # Show a sample of the HTML around student rows
                lines = html_content.split('\n')
                for i, line in enumerate(lines):
                    if 'student-name' in line:
                        print(f"Line {i}: {line.strip()}")
                        if i+1 < len(lines):
                            print(f"Line {i+1}: {lines[i+1].strip()}")
                        break
                
                # Save full HTML for inspection
                with open('debug_grading.html', 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print("\n✓ Full HTML saved to debug_grading.html")
                        
            else:
                print("✗ Failed to access grading interface")
                print(f"Response: {response.data.decode('utf-8')[:500]}")

if __name__ == '__main__':
    test_grading_interface_detailed()