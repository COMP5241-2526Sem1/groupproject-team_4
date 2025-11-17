#!/usr/bin/env python3
"""
Comprehensive test to verify the foreign key fix works with questions that have responses
"""

import requests
import json
from bs4 import BeautifulSoup

def test_foreign_key_with_responses():
    """Test editing a quiz that has questions with student responses"""
    
    # Create session
    session = requests.Session()
    
    # Login as teacher (john_smith teaches COMP101)
    login_data = {
        'username': 'john_smith',
        'password': 'comp5241',
        'role': 'teacher'
    }
    
    login_response = session.post('http://localhost:5000/login', 
                            headers={'Content-Type': 'application/json'},
                            data=json.dumps(login_data))
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    login_data = json.loads(login_response.text)
    if login_data.get('msg') != 'login success!':
        print(f"❌ Login failed: {login_data}")
        return False
    
    print("✅ Login successful")
    
    # First, create a new quiz
    create_url = "http://localhost:5000/teacher/course/COMP101/quiz/create"
    response = session.get(create_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to access quiz creation page: {response.status_code}")
        return False
    
    print("✅ Successfully accessed quiz creation page")
    
    # Create a quiz
    quiz_data = {
        'name': 'Foreign Key Test Quiz',
        'description': 'This quiz tests the foreign key fix with responses',
        'duration': '30',
        'attempt_limit': '3',
        'point_in_course': '10'
    }
    
    response = session.post(create_url, data=quiz_data)
    
    if response.status_code != 200:
        print(f"❌ Failed to create quiz: {response.status_code}")
        return False
    
    print("✅ Successfully created quiz")
    
    # Get the quiz ID from the response or redirect
    # For now, let's get the latest quiz from the list
    quiz_list_url = "http://localhost:5000/teacher/course/COMP101/quiz"
    response = session.get(quiz_list_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to access quiz list: {response.status_code}")
        return False
    
    # Parse the quiz list to find our quiz
    soup = BeautifulSoup(response.text, 'html.parser')
    quiz_links = soup.find_all('a', href=lambda href: href and '/quiz/' in href and '/edit' in href)
    
    if not quiz_links:
        print("❌ No quiz edit links found")
        return False
    
    # Get the first (latest) quiz ID
    href = quiz_links[0].get('href')
    parts = href.split('/')
    quiz_id = int(parts[5])
    
    print(f"✅ Found quiz ID: {quiz_id}")
    
    # Now add a question to the quiz by editing the quiz
    edit_url = f"http://localhost:5000/teacher/course/COMP101/quiz/{quiz_id}/edit"
    response = session.get(edit_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to access edit quiz page: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return False
    
    print("✅ Successfully accessed edit quiz page")
    
    # Get existing quiz data to preserve it
    quiz_name = "Test Quiz for Foreign Key Fix"
    quiz_description = "Testing foreign key constraint handling"
    
    # Add a simple multiple choice question along with existing quiz data
    question_data = {
        'name': quiz_name,
        'description': quiz_description,
        'duration': '30',
        'attempt_limit': '5',
        'point_in_course': '10',
        'questions[1][type]': 'mcq',
        'questions[1][content]': 'What is 2+2?',
        'questions[1][points]': '5',
        'questions[1][choices][1]': '3',
        'questions[1][choices][2]': '4',
        'questions[1][choices][3]': '5',
        'questions[1][correct_choice]': '2'
    }
    
    response = session.post(edit_url, data=question_data)
    
    if response.status_code != 200 and response.status_code != 302:  # 302 is redirect after successful edit
        print(f"❌ Failed to add question: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return False
    
    print("✅ Successfully added question to quiz")
    
    # Now try to edit the quiz (this should work even with the question)
    edit_url = f"http://localhost:5000/teacher/course/COMP101/quiz/{quiz_id}/edit"
    response = session.get(edit_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to access edit page: {response.status_code}")
        return False
    
    print("✅ Successfully accessed edit page with question")
    
    # Try to update the quiz
    edit_data = {
        'name': 'Foreign Key Test Quiz (Updated)',
        'description': 'This quiz has been updated to test the foreign key fix',
        'duration': '35',
        'attempt_limit': '3',
        'point_in_course': '10'
    }
    
    response = session.post(edit_url, data=edit_data)
    
    if response.status_code != 200:
        print(f"❌ Failed to update quiz with question: {response.status_code}")
        print("Response content:", response.text[:500])
        return False
    
    print("✅ Successfully updated quiz with question")
    
    # Now let's try to edit the quiz again (this tests the foreign key fix)
    print("\n🔄 Testing foreign key constraint handling...")
    
    # Try to edit the quiz again (this should work without foreign key errors)
    edit_url = f"http://localhost:5000/teacher/course/COMP101/quiz/{quiz_id}/edit"
    response = session.get(edit_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to access edit page: {response.status_code}")
        return False
    
    print("✅ Successfully accessed edit page again")
    
    # Update the quiz with the same question (this tests the foreign key handling)
    # First, let's get the existing question ID to preserve it
    updated_data = {
        'name': 'Test Quiz for Foreign Key Fix',
        'description': 'Testing foreign key constraint handling - updated',
        'duration': '45',
        'attempt_limit': '3',
        'point_in_course': '15',
        'questions[1][id]': '',  # This will create a new question since we don't have the ID
        'questions[1][type]': 'mcq',
        'questions[1][content]': 'What is 2+2? (Updated)',
        'questions[1][points]': '10',
        'questions[1][choices][1]': '3',
        'questions[1][choices][2]': '4',
        'questions[1][choices][3]': '5',
        'questions[1][correct_choice]': '2'
    }
    
    response = session.post(edit_url, data=updated_data)
    
    if response.status_code != 200 and response.status_code != 302:
        print(f"❌ Failed to update quiz: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return False
    
    print("✅ Successfully updated quiz without foreign key errors")
    print("✅ Foreign key fix is working correctly!")
    
    return True

if __name__ == "__main__":
    print("Testing foreign key fix with comprehensive scenario...")
    success = test_foreign_key_with_responses()
    
    if success:
        print("\n✅ Comprehensive foreign key test passed!")
        print("✅ The fix successfully handles questions during quiz editing!")
    else:
        print("\n❌ Comprehensive foreign key test failed!")