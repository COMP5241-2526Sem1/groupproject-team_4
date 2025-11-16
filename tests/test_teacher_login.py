import requests
import sys

# Test login and then access teacher quiz route
session = requests.Session()

# Login as teacher
login_data = {
    'username': 'john_smith',
    'password': 'password123'
}

print("Attempting to login as teacher...")
try:
    login_response = session.post('http://localhost:5000/login', json=login_data, headers={'Content-Type': 'application/json'})
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        print("Login successful, now testing teacher quiz route...")
        
        # Test teacher quiz info route
        quiz_response = session.get('http://localhost:5000/teacher/course/PHYS101/quiz/14')
        print(f"Teacher quiz route status: {quiz_response.status_code}")
        
        if quiz_response.status_code == 200:
            print("✅ SUCCESS: Teacher quiz route is working without AttributeError!")
            # Check if we got the teacher view content
            if "Teacher View:" in quiz_response.text:
                print("✅ SUCCESS: Teacher view content is displayed correctly")
            else:
                print("⚠️  WARNING: Content might not be the teacher view")
        else:
            print(f"❌ FAILED: Teacher quiz route returned status {quiz_response.status_code}")
            print(f"Response: {quiz_response.text[:200]}...")
    else:
        print(f"❌ FAILED: Login failed with status {login_response.status_code}")
        print(f"Response: {login_response.text[:200]}...")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

print("Test completed successfully!")