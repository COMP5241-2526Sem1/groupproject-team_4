import requests
import json
import re

# Test the edge cases where course_code might be missing
BASE_URL = "http://localhost:5000"
login_data = {
    'username': 'a',
    'password': 'comp5241',
    'role': 'student'
}

session = requests.Session()
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("🧪 Testing edge cases for missing course_code...")

# Login
login_response = session.post(f"{BASE_URL}/login", data=json.dumps(login_data), headers=headers)
if login_response.status_code == 200 and 'login success' in login_response.text:
    print("✅ Login successful!")
    
    # Test 1: Access non-existent quiz
    print("\n1. Testing non-existent quiz...")
    fake_quiz_response = session.get(f"{BASE_URL}/course/COMP101/quiz/999")
    print(f"   Non-existent quiz status: {fake_quiz_response.status_code}")
    
    if fake_quiz_response.status_code == 404:
        # Check if View Results button exists and has correct URL
        if 'View Results' in fake_quiz_response.text:
            results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', fake_quiz_response.text, re.IGNORECASE)
            if results_url_match:
                href = results_url_match.group(1)
                print(f"   View Results URL: {href}")
                if '/course//quiz/' in href:
                    print("❌ ISSUE: Empty course code found in non-existent quiz case!")
                else:
                    print("✅ Course code appears correctly")
        else:
            print("   No View Results button found (expected for non-existent quiz)")
    
    # Test 2: Try to access quiz with wrong course code
    print("\n2. Testing quiz with wrong course code...")
    wrong_course_response = session.get(f"{BASE_URL}/course/INVALID/quiz/4")
    print(f"   Wrong course code status: {wrong_course_response.status_code}")
    
    # Test 3: Test a quiz that might not be available (time-based)
    print("\n3. Testing potentially unavailable quiz...")
    
    # Let's check what quizzes exist and their availability
    from app import app
    from models import Quiz, Course
    
    with app.app_context():
        # Find a quiz that might be time-restricted
        quizzes = Quiz.query.all()
        for quiz in quizzes:
            if quiz.start_datetime or quiz.end_datetime:
                print(f"   Found time-restricted quiz: {quiz.name} (ID: {quiz.id})")
                print(f"   Start: {quiz.start_datetime}, End: {quiz.end_datetime}")
                
                # Test this quiz
                quiz_response = session.get(f"{BASE_URL}/course/{quiz.course_code}/quiz/{quiz.id}")
                print(f"   Quiz {quiz.id} status: {quiz_response.status_code}")
                
                if quiz_response.status_code == 400:
                    if 'View Results' in quiz_response.text:
                        results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', quiz_response.text, re.IGNORECASE)
                        if results_url_match:
                            href = results_url_match.group(1)
                            print(f"   View Results URL: {href}")
                            if '/course//quiz/' in href:
                                print("❌ ISSUE: Empty course code found in unavailable quiz case!")
                            else:
                                print("✅ Course code appears correctly")
                break
    
    print("\n4. Testing max attempts scenario...")
    
    # Test quiz 5 where user 'a' has already used all attempts
    quiz5_response = session.get(f"{BASE_URL}/course/COMP101/quiz/5")
    print(f"   Quiz 5 (max attempts) status: {quiz5_response.status_code}")
    
    if quiz5_response.status_code == 200 and 'View Results' in quiz5_response.text:
        results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', quiz5_response.text, re.IGNORECASE)
        if results_url_match:
            href = results_url_match.group(1)
            print(f"   View Results URL: {href}")
            if '/course//quiz/' in href:
                print("❌ ISSUE: Empty course code found in max attempts case!")
            else:
                print("✅ Course code appears correctly")
    
else:
    print("❌ Login failed")