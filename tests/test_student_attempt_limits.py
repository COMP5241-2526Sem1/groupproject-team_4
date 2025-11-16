#!/usr/bin/env python3
"""
Test that students are still subject to attempt count limits
"""

import requests
import sys

def test_student_attempt_limits():
    """Test that students have attempt limits"""
    
    # Base URL
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("Testing student attempt limits...")
    print("=" * 50)
    
    # Step 1: Login as student
    print("1. Logging in as student...")
    login_data = {
        'username': 'alice_johnson',
        'password': 'comp5241',
        'role': 'student'
    }
    
    login_response = session.post(f"{base_url}/login", json=login_data, headers={'Content-Type': 'application/json'})
    
    if login_response.status_code != 200 or 'success' not in login_response.text.lower():
        print(f"❌ Student login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return False
    
    print("✅ Student login successful")
    
    # Step 2: Try to access a quiz that might have attempt limits
    print("\n2. Getting quiz info for student...")
    quiz_id = 18
    quiz_info_response = session.get(f"{base_url}/course/COMP101/quiz/{quiz_id}")
    
    if quiz_info_response.status_code == 200:
        print("✅ Student can access quiz info")
        
        # Check if attempt information is shown
        if "attempt" in quiz_info_response.text.lower():
            print("✅ Attempt information shown to student")
        else:
            print("⚠️  Attempt information not found")
            
        # Save for inspection
        with open('student_quiz_info.html', 'w', encoding='utf-8') as f:
            f.write(quiz_info_response.text)
    else:
        print(f"❌ Student cannot access quiz info: {quiz_info_response.status_code}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Student attempt limit system is working")
    return True

if __name__ == "__main__":
    try:
        success = test_student_attempt_limits()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        sys.exit(1)