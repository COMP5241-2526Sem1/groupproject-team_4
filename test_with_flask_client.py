import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from app import app
from models.user import User
from models.quiz import Quiz
from models.submission import Submission
from models.course_enrollment import CourseEnrollment
from database import db

def test_results_preview_with_session():
    """Test results preview using Flask test client with proper session management"""
    
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    
    with app.test_client() as client:
        with app.app_context():
            # Find user 'a' who we know completed quiz 5
            user_a = User.query.filter_by(username='a').first()
            if not user_a:
                print("User 'a' not found!")
                return False
                
            print(f"Testing with user: {user_a.username} (ID: {user_a.id})")
            
            # Manually set the session user_id
            with client.session_transaction() as sess:
                sess['user_id'] = user_a.id
            
            # Test quiz 5 (Functions and Modules Quiz) - user 'a' completed all attempts
            print("Testing Quiz 5 (Functions and Modules Quiz)...")
            response = client.get('/course/COMP101/quiz/5')
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Length: {len(response.data)}")
            
            # Decode response data
            response_text = response.data.decode('utf-8')
            
            # Check if we got the login page or actual quiz page
            if "Sign In" in response_text:
                print("❌ Still getting login page - session not working")
                return False
            
            # Check for results preview
            if "Your Results Preview" in response_text:
                print("✅ Results preview is displayed!")
                
                if "Score:" in response_text:
                    print("✅ Score is shown")
                if "Question" in response_text:
                    print("✅ Question details are visible")
                if "Class Statistics" in response_text:
                    print("✅ Class statistics are shown")
                    
                # Save the response for inspection
                with open("flask_client_quiz5_response.html", "w", encoding="utf-8") as f:
                    f.write(response_text)
                print("Response saved to flask_client_quiz5_response.html")
                
            else:
                print("❌ Results preview not found")
                
                # Check what message we get instead
                if "attempts remaining" in response_text:
                    print("Found 'attempts remaining' message")
                if "Quiz feedback is limited" in response_text:
                    print("Found 'Quiz feedback is limited' message")
                    
                # Save the response to see what's happening
                with open("flask_client_no_preview.html", "w", encoding="utf-8") as f:
                    f.write(response_text)
                print("Response saved to flask_client_no_preview.html")
            
            # Also test quiz 4 to compare
            print("\nTesting Quiz 4 (Python Basics Quiz) for comparison...")
            response4 = client.get('/course/COMP101/quiz/4')
            print(f"Quiz 4 Status Code: {response4.status_code}")
            
            if "Your Results Preview" in response4.data.decode('utf-8'):
                print("✅ Quiz 4 shows results preview")
            else:
                print("❌ Quiz 4 does not show results preview")
                
            return True

if __name__ == "__main__":
    success = test_results_preview_with_session()
    sys.exit(0 if success else 1)