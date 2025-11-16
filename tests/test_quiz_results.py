#!/usr/bin/env python3
"""Test script to check quiz results page"""

import requests
from werkzeug.security import check_password_hash

# Test the quiz results page with proper URL format
base_url = "http://localhost:5000"

# First, let's login as a student
login_data = {
    'username': 'alice_johnson',
    'password': 'password123'  # Try the common password
}

session = requests.Session()

# Login
login_response = session.post(f"{base_url}/login", data=login_data)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    # Try to access quiz results with proper course code
    # We need to know which course the student is enrolled in
    # Let's try COMP101 first (common course code)
    course_code = "COMP101"
    quiz_id = 7
    
    results_url = f"{base_url}/course/{course_code}/quiz/{quiz_id}/results"
    print(f"Testing URL: {results_url}")
    
    results_response = session.get(results_url)
    print(f"Quiz results status: {results_response.status_code}")
    
    if results_response.status_code == 200:
        print("✅ Quiz results page loaded successfully")
        # Check if it's the actual results page or an error page
        if "Quiz Results" in results_response.text:
            print("✅ Found 'Quiz Results' in page content")
        else:
            print("⚠️  Page loaded but no 'Quiz Results' found - might be an error page")
            # Print first few lines to see what we got
            lines = results_response.text.split('\n')[:10]
            for line in lines:
                if line.strip():
                    print(f"  {line.strip()}")
    elif results_response.status_code == 404:
        print("❌ Quiz results page not found")
        print("Possible issues:")
        print("- Course code might be wrong")
        print("- Quiz ID might not exist")
        print("- Student might not be enrolled in the course")
        print("- Student might not have submitted the quiz")
    elif results_response.status_code == 403:
        print("❌ Access forbidden - student not enrolled or no submission")
    else:
        print(f"❌ Unexpected status code: {results_response.status_code}")
        
else:
    print("❌ Login failed - cannot test quiz results")

# Also test password directly
print("\n--- Testing password directly ---")
from app import app, User
with app.app_context():
    user = User.query.filter_by(username='alice_johnson').first()
    if user:
        print(f"Found user: {user.username}, role: {user.role}")
        if check_password_hash(user.password_hash, 'password123'):
            print("✅ Password 'password123' is correct")
        else:
            print("❌ Password 'password123' is incorrect")
            # Test other common passwords
            test_passwords = ['password', '123456', 'student', 'alice', 'alice_johnson']
            for pwd in test_passwords:
                if check_password_hash(user.password_hash, pwd):
                    print(f"✅ Password is: {pwd}")
                    break
            else:
                print("❌ None of the common passwords worked")
    else:
        print("❌ User not found")