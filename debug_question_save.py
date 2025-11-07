import requests
import json

# Test script to debug question saving issue

# Login data - using the debug teacher account we created
login_data = {
    'username': 'debug_teacher',
    'password': 'debug123',
    'role': 'teacher'
}

session = requests.Session()
login_response = session.post('http://127.0.0.1:5000/login', json=login_data)
print(f"Login status: {login_response.status_code}")
if login_response.status_code == 200:
    print(f"Login response: {login_response.json()}")

# Create a simple quiz with one question
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

print("\nSending quiz creation data:")
for key, value in create_data.items():
    print(f"  {key}: {value}")

create_response = session.post('http://127.0.0.1:5000/teacher/course/DEBUG101/quiz/create', data=create_data)
print(f"\nCreate quiz status: {create_response.status_code}")
print(f"Response headers: {create_response.headers}")

# Check if we got redirected to quiz list
if create_response.status_code == 200:
    print(f"Response content length: {len(create_response.text)}")
    if 'Quiz created successfully' in create_response.text:
        print("✅ Success message found in response")
    else:
        print("❌ No success message found")
        print("First 500 chars of response:", create_response.text[:500])