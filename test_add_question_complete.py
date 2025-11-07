#!/usr/bin/env python3
"""
Comprehensive test for Add Question functionality
"""

import requests
import json

def test_add_question_functionality():
    """Test the complete Add Question functionality flow"""
    
    base_url = "http://127.0.0.1:5000"
    session = requests.Session()
    
    print("🧪 Testing Add Question Functionality")
    print("=" * 50)
    
    # Step 1: Test login
    print("1️⃣ Testing login...")
    login_data = {
        "username": "test_teacher",
        "password": "test123",
        "role": "teacher"
    }
    
    try:
        response = session.post(f"{base_url}/login", 
                              json=login_data,
                              headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            print("✅ Login successful")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False
    
    # Step 2: Test accessing quiz edit page
    print("\n2️⃣ Testing quiz edit page access...")
    try:
        response = session.get(f"{base_url}/teacher/course/CS101/quiz/9/edit")
        
        if response.status_code == 200:
            print("✅ Quiz edit page accessible")
            print(f"   Page title: {'Edit Quiz' if 'Edit Quiz' in response.text else 'Title not found'}")
            
            # Check for Add Question button
            if 'add-question-btn' in response.text:
                print("✅ Add Question button found in HTML")
            else:
                print("❌ Add Question button NOT found in HTML")
                
            # Check for addQuestion function
            if 'function addQuestion()' in response.text:
                print("✅ addQuestion() function found in JavaScript")
            else:
                print("❌ addQuestion() function NOT found in JavaScript")
                # Debug: check what's actually in the response
                if 'addQuestion' in response.text:
                    print(f"   Found 'addQuestion' text but not exact pattern")
                    # Find lines containing addQuestion
                    lines = response.text.split('\n')
                    addquestion_lines = [line.strip() for line in lines if 'addQuestion' in line]
                    if addquestion_lines:
                        print(f"   Lines with addQuestion: {addquestion_lines[:3]}")
                else:
                    print("   No 'addQuestion' text found at all")
                
        else:
            print(f"❌ Quiz edit page access failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Quiz edit page access error: {e}")
        return False
    
    # Step 3: Test getting quiz questions (API endpoint)
    print("\n3️⃣ Testing quiz questions API...")
    try:
        response = session.get(f"{base_url}/teacher/course/CS101/quiz/9/questions",
                             headers={"Accept": "application/json"})
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Quiz questions API working")
            print(f"   Questions count: {len(data.get('questions', []))}")
        else:
            print(f"❌ Quiz questions API failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Quiz questions API error: {e}")
    
    # Step 4: Test the actual functionality by simulating form submission
    print("\n4️⃣ Testing quiz update with new question...")
    try:
        # Get the current quiz data first
        response = session.get(f"{base_url}/teacher/course/CS101/quiz/9/edit")
        if response.status_code != 200:
            print("❌ Could not get quiz edit page for form data")
            return False
        
        # Prepare form data with a new question
        form_data = {
            'name': 'Test Quiz',
            'description': 'Test quiz for Add Question functionality',
            'duration': '60',
            'attempt_limit': '5',
            'point': '100',
            'point_in_course': '0',
            'question_visible': 'false',
            'student_response_visible': 'false',
            'sample_response_visible': 'false',
            'class_response_visible': 'false',
            'questions[1][type]': 'mcq',
            'questions[1][content]': 'What is 2+2?',
            'questions[1][points]': '10',
            'questions[1][choices][1]': '3',
            'questions[1][choices][2]': '4',
            'questions[1][correct_choice]': '2'
        }
        
        response = session.post(f"{base_url}/teacher/course/CS101/quiz/9/edit", 
                              data=form_data)
        
        if response.status_code == 200 or response.status_code == 302:  # 302 is redirect after successful update
            print("✅ Quiz update with new question successful")
        else:
            print(f"❌ Quiz update failed: {response.status_code}")
            print(f"   Response: {response.text[:300]}...")
            
    except Exception as e:
        print(f"❌ Quiz update error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Add Question Functionality Test Complete!")
    return True

if __name__ == "__main__":
    test_add_question_functionality()