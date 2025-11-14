#!/usr/bin/env python3
"""Simple test to check what's wrong with the quiz results URL"""

import requests

base_url = "http://localhost:5000"

# Let's try the debug teacher account that we know works
login_data = {
    'username': 'debug_teacher',
    'password': 'debug123'
}

session = requests.Session()

# Login
login_response = session.post(f"{base_url}/login", data=login_data)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    print("✅ Login successful")
    
    # Try to access quiz results with DEBUG101 course (which we know exists)
    course_code = "DEBUG101"
    quiz_id = 10  # The quiz we created earlier
    
    results_url = f"{base_url}/course/{course_code}/quiz/{quiz_id}/results"
    print(f"Testing URL: {results_url}")
    
    results_response = session.get(results_url)
    print(f"Quiz results status: {results_response.status_code}")
    
    if results_response.status_code == 200:
        print("✅ Quiz results page loaded successfully")
        if "Quiz Results" in results_response.text:
            print("✅ Found 'Quiz Results' in page content")
        else:
            print("⚠️  Page loaded but no 'Quiz Results' found")
            # Show first few lines
            lines = results_response.text.split('\n')[:5]
            for line in lines:
                if line.strip():
                    print(f"  {line.strip()}")
    elif results_response.status_code == 404:
        print("❌ Quiz results page not found")
    elif results_response.status_code == 403:
        print("❌ Access forbidden")
        print("This might be because:")
        print("- User is not enrolled in the course")
        print("- User has not submitted the quiz")
        print("- Quiz visibility settings prevent access")
    else:
        print(f"❌ Unexpected status code: {results_response.status_code}")
        
    # Also try with COMP101 (which should exist based on SQL data)
    comp_url = f"{base_url}/course/COMP101/quiz/4/results"
    print(f"\nAlso testing: {comp_url}")
    comp_response = session.get(comp_url)
    print(f"COMP101 quiz results status: {comp_response.status_code}")
    
else:
    print("❌ Login failed")