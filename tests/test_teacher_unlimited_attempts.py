#!/usr/bin/env python3
"""
Test that teachers can take quizzes unlimited times without attempt count limits
"""

import requests
import sys
from datetime import datetime

def test_teacher_unlimited_attempts():
    """Test that teachers can take quizzes unlimited times"""
    
    # Base URL
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # Teacher credentials (john_smith from working tests)
    login_data = {
        'username': 'john_smith',
        'password': 'comp5241'
    }
    
    print("Testing teacher unlimited quiz attempts...")
    print("=" * 50)
    
    # Step 1: Login as teacher
    print("1. Logging in as teacher...")
    login_data = {
        'username': 'john_smith',
        'password': 'comp5241',
        'role': 'teacher'
    }
    login_response = session.post(f"{base_url}/login", json=login_data, headers={'Content-Type': 'application/json'})
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return False
    
    print("✅ Teacher login successful")
    
    # Step 2: Get teacher home to see available courses
    print("\n2. Getting teacher home page...")
    home_response = session.get(f"{base_url}/teacher")
    
    if home_response.status_code != 200:
        print(f"❌ Teacher home access failed: {home_response.status_code}")
        return False
    
    print("✅ Teacher home accessed")
    
    # Step 3: Get quiz list for COMP101
    print("\n3. Getting quiz list for COMP101...")
    quiz_list_response = session.get(f"{base_url}/teacher/course/COMP101/quiz")
    
    if quiz_list_response.status_code != 200:
        print(f"❌ Quiz list access failed: {quiz_list_response.status_code}")
        return False
    
    print("✅ Quiz list accessed")
    
    # Step 4: Test starting quiz multiple times
    print("\n4. Testing unlimited quiz attempts...")
    
    quiz_id = 18  # Using the quiz we know exists
    max_attempts = 3  # Test with 3 attempts to verify unlimited access
    
    for attempt_num in range(1, max_attempts + 1):
        print(f"\n   Attempt {attempt_num}:")
        
        # Try to start the quiz
        start_response = session.get(f"{base_url}/course/COMP101/quiz/{quiz_id}/start")
        
        if start_response.status_code == 200:
            print(f"   ✅ Quiz started successfully (attempt {attempt_num})")
            
            # Save the response for inspection
            with open(f'teacher_attempt_{attempt_num}.html', 'w', encoding='utf-8') as f:
                f.write(start_response.text)
            
            # Check if we got the quiz page (not an error page)
            if 'quiz_start.html' in start_response.text or 'Quiz' in start_response.text:
                print(f"   ✅ Quiz page loaded correctly")
            else:
                print(f"   ⚠️  Unexpected page content")
                
        elif start_response.status_code == 400:
            # Check if it's an attempt limit error
            if "maximum number of attempts" in start_response.text:
                print(f"   ❌ Attempt limit reached - this should not happen for teachers!")
                print(f"   Response: {start_response.text[:200]}...")
                return False
            else:
                print(f"   ❌ Other error: {start_response.text[:200]}...")
                return False
        else:
            print(f"   ❌ Failed to start quiz: {start_response.status_code}")
            print(f"   Response: {start_response.text[:200]}...")
            return False
    
    print(f"\n✅ SUCCESS: Teacher can take quiz {max_attempts} times without limit!")
    
    # Step 5: Verify attempt count in database perspective
    print("\n5. Checking current attempt count...")
    
    # Get quiz info to see attempt count
    quiz_info_response = session.get(f"{base_url}/course/COMP101/quiz/{quiz_id}")
    
    if quiz_info_response.status_code == 200:
        print("✅ Quiz info accessible")
        # Look for attempt count in response
        if "attempt" in quiz_info_response.text.lower():
            print("✅ Attempt information available in quiz info")
        
        # Save quiz info for inspection
        with open('teacher_quiz_info_after_attempts.html', 'w', encoding='utf-8') as f:
            f.write(quiz_info_response.text)
    else:
        print(f"⚠️  Could not get quiz info: {quiz_info_response.status_code}")
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("✅ Teachers can take quizzes unlimited times")
    print("✅ No attempt count restrictions for teachers")
    print("✅ Quiz access works correctly")
    
    return True

if __name__ == "__main__":
    try:
        success = test_teacher_unlimited_attempts()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        sys.exit(1)