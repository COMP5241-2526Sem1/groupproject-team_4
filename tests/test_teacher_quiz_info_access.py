#!/usr/bin/env python3
"""
Test script to verify that teachers can access quiz info pages for their courses.
"""

import requests
import json

# Base URL for the Flask application
base_url = "http://localhost:5000"

# Create a session to maintain cookies
session = requests.Session()

def test_teacher_quiz_info_access():
    """Test that teachers can access quiz info pages for their courses."""
    
    print("🧪 Testing Teacher Quiz Info Access")
    print("=" * 50)
    
    # 1. Login as teacher
    print("\n1️⃣ Logging in as teacher...")
    login_data = {
        'username': 'john_smith',
        'password': 'comp5241',
        'role': 'teacher'
    }
    
    response = session.post(f"{base_url}/login", 
                           json=login_data,
                           headers={'Content-Type': 'application/json'})
    
    if response.status_code != 200 or 'success' not in response.text.lower():
        print(f"❌ Login failed: {response.status_code}")
        print(f"Response: {response.text}")
        return False
    
    print("✅ Login successful")
    
    # 2. Get list of teacher's courses to find a valid course and quiz
    print("\n2️⃣ Getting teacher's courses...")
    teacher_home_response = session.get(f"{base_url}/teacher")
    
    if teacher_home_response.status_code != 200:
        print(f"❌ Failed to access teacher home: {teacher_home_response.status_code}")
        return False
    
    print("✅ Teacher home accessed")
    
    # 3. First get the teacher quiz list to see what quizzes exist
    print("\n3️⃣ Getting teacher quiz list for COMP101...")
    teacher_quiz_list_url = f"{base_url}/teacher/course/COMP101/quiz"
    quiz_list_response = session.get(teacher_quiz_list_url)
    
    if quiz_list_response.status_code != 200:
        print(f"❌ Failed to access teacher quiz list: {quiz_list_response.status_code}")
        return False
    
    print("✅ Teacher quiz list accessed")
    
    # Extract quiz IDs from the quiz list page
    import re
    quiz_links = re.findall(r'href="/course/COMP101/quiz/(\d+)"', quiz_list_response.text)
    quiz_ids = list(set(quiz_links))  # Remove duplicates
    
    if not quiz_ids:
        print("❌ No quizzes found for COMP101")
        return False
    
    print(f"Found quizzes for COMP101: {quiz_ids}")
    
    # 4. Try to access quiz info pages for available quizzes
    print("\n4️⃣ Testing quiz info access for teacher's course...")
    
    success_count = 0
    for quiz_id in quiz_ids[:2]:  # Test first 2 quizzes
        quiz_info_url = f"{base_url}/course/COMP101/quiz/{quiz_id}"
        print(f"Testing: {quiz_info_url}")
        
        quiz_response = session.get(quiz_info_url)
        print(f"Quiz info response status: {quiz_response.status_code}")
        
        if quiz_response.status_code == 200:
            print("✅ Teacher can access quiz info page!")
            success_count += 1
            
            # Save the first successful response for inspection
            if success_count == 1:
                with open('teacher_quiz_info_success.html', 'w', encoding='utf-8') as f:
                    f.write(quiz_response.text)
                print("💾 Saved response to teacher_quiz_info_success.html")
                
        elif quiz_response.status_code == 403:
            print("❌ Teacher cannot access quiz info page (403 Forbidden)")
            print(f"Response: {quiz_response.text[:200]}")
            return False
        else:
            print(f"❌ Unexpected response: {quiz_response.status_code}")
    
    if success_count > 0:
        print(f"\n✅ Successfully accessed {success_count} quiz info pages!")
        return True
    else:
        print("\n❌ Could not access any quiz info pages")
        return False

if __name__ == "__main__":
    success = test_teacher_quiz_info_access()
    
    if success:
        print("\n🎉 SUCCESS: Teachers can access quiz info pages!")
    else:
        print("\n❌ FAILED: Teachers cannot access quiz info pages")
    
    session.close()