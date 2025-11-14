import requests
import json

# Test script to find correct login credentials

session = requests.Session()

# Test different teacher users and passwords
test_users = [
    {'username': 'debug_teacher', 'password': 'debug123', 'role': 'teacher'},
]

for user in test_users:
    print(f"\nTesting {user['username']}...")
    login_response = session.post('http://127.0.0.1:5000/login', json=user)
    print(f"Login status: {login_response.status_code}")
    if login_response.status_code == 200:
        print(f"✅ Login successful: {login_response.json()}")
        # Test quiz creation
        create_data = {
            'name': 'Debug Quiz',
            'description': 'Testing question saving',
            'duration': 30,
            'attempt_limit': 5,
            'point': 100,
            'point_in_course': 0,
            'question_visible': 'true',
            'student_response_visible': 'true',
            'sample_response_visible': 'true',
            'class_response_visible': 'true',
            'questions[1][type]': 'mcq',
            'questions[1][content]': 'What is 2+2?',
            'questions[1][points]': '10',
            'questions[1][choices][1]': '3',
            'questions[1][choices][2]': '4',
            'questions[1][choices][3]': '5',
            'questions[1][correct_choice]': '2'
        }
        
        create_response = session.post('http://127.0.0.1:5000/teacher/course/DEBUG101/quiz/create', data=create_data)
        print(f"Quiz creation status: {create_response.status_code}")
        if 'Quiz created successfully' in create_response.text:
            print("✅ Quiz created successfully!")
        else:
            print("❌ Quiz creation may have failed")
            print("First 200 chars:", create_response.text[:200])
        break
    else:
        print(f"❌ Login failed: {login_response.text[:100]}")