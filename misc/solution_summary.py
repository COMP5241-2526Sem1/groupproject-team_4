"""
SOLUTION SUMMARY: Quiz Creation Issue Resolution
==================================================

PROBLEM:
- Quiz creation was failing with 404 and 403 errors
- Login was failing with incorrect credentials
- Quiz endpoint was using wrong URL

ROOT CAUSES IDENTIFIED:
1. Incorrect login credentials (john_smith/password123 didn't work)
2. Wrong login endpoint (was using /auth/login instead of /login)
3. Teacher user didn't have any courses assigned
4. Wrong quiz creation endpoint (was using generic /quiz/create instead of teacher-specific)
5. Missing course ownership validation

SOLUTIONS IMPLEMENTED:
1. Created debug_teacher account with password 'debug123'
2. Created DEBUG101 course assigned to debug_teacher
3. Used correct login endpoint: http://127.0.0.1:5000/login
4. Used correct quiz creation endpoint: /teacher/course/DEBUG101/quiz/create
5. Added all required form fields including visibility settings

VERIFICATION:
- Login successful with debug_teacher credentials
- Quiz creation successful with 200 status
- Quiz and questions properly saved to database
- Multiple choice questions with correct answers working

WORKING EXAMPLE:
"""

import requests

def create_quiz_example():
    # Create session
    session = requests.Session()
    
    # Login with debug teacher
    login_data = {
        'username': 'debug_teacher',
        'password': 'debug123',
        'role': 'teacher'
    }
    
    login_response = session.post('http://127.0.0.1:5000/login', data=login_data)
    print(f"Login: {login_response.status_code} - {login_response.json()}")
    
    # Create quiz with questions
    quiz_data = {
        'name': 'Sample Quiz',
        'description': 'A sample quiz demonstrating the working solution',
        'duration': 30,
        'attempt_limit': 5,
        'point': 100,
        'point_in_course': 0,
        'question_visible': 'true',
        'student_response_visible': 'true',
        'sample_response_visible': 'true',
        'class_response_visible': 'true',
        'questions[1][type]': 'mcq',
        'questions[1][content]': 'What is the capital of France?',
        'questions[1][points]': '10',
        'questions[1][choices][1]': 'London',
        'questions[1][choices][2]': 'Paris',
        'questions[1][choices][3]': 'Berlin',
        'questions[1][correct_choice]': '2'
    }
    
    quiz_response = session.post('http://127.0.0.1:5000/teacher/course/DEBUG101/quiz/create', data=quiz_data)
    print(f"Quiz creation: {quiz_response.status_code}")
    
    if 'Quiz created successfully' in quiz_response.text:
        print("✅ SUCCESS: Quiz created successfully!")
    else:
        print(f"❌ Failed: {quiz_response.text[:200]}")

if __name__ == "__main__":
    create_quiz_example()