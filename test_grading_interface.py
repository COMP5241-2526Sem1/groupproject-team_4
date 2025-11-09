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

def test_grading_interface():
    """Test the teacher grading interface with the updated template"""
    
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
                
                # Check for student username display
                if 'daniel_miller' in html_content:
                    print("✓ Student username is displayed correctly")
                else:
                    print("✗ Student username not found")
                
                # Check for simplified layout (no flexbox container)
                if 'grade-input-group' not in html_content:
                    print("✓ Simplified layout (no grade-input-group wrapper)")
                else:
                    print("✗ Still has grade-input-group wrapper")
                
                # Check for table structure
                if '<table class="grading-table">' in html_content:
                    print("✓ Table structure is present")
                else:
                    print("✗ Table structure missing")
                
                # Check for question content
                if 'Q4Q1' in html_content:
                    print("✓ Question content is displayed")
                else:
                    print("✗ Question content not found")
                
                # Check for simplified styling
                if 'border: 1px solid #ddd' in html_content:
                    print("✓ Simplified styling applied")
                else:
                    print("✗ Simplified styling not applied")
                
                print("\n--- Sample HTML Content ---")
                # Show a sample of the student row
                lines = html_content.split('\n')
                for i, line in enumerate(lines):
                    if 'daniel_miller' in line:
                        print('\n'.join(lines[max(0, i-2):min(len(lines), i+5)]))
                        break
                        
            else:
                print("✗ Failed to access grading interface")
                print(f"Response: {response.data.decode('utf-8')[:500]}")

if __name__ == '__main__':
    test_grading_interface()