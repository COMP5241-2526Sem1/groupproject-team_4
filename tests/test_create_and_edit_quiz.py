#!/usr/bin/env python3
"""
Test script to create a quiz and then edit it to verify the foreign key fix works
"""

import requests
import json
from bs4 import BeautifulSoup

def test_create_and_edit_quiz():
    """Create a quiz, add some questions, then try to edit it"""
    
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
    
    # First, try to access the quiz creation page
    create_url = "http://localhost:5000/teacher/course/COMP101/quiz/create"
    response = session.get(create_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to access quiz creation page: {response.status_code}")
        return False
    
    print("✅ Successfully accessed quiz creation page")
    
    # Create a simple quiz
    quiz_data = {
        'name': 'Test Quiz for Foreign Key Fix',
        'description': 'This quiz is created to test the foreign key fix',
        'duration': '30',
        'attempt_limit': '3',
        'point_in_course': '10'
    }
    
    response = session.post(create_url, data=quiz_data)
    
    if response.status_code != 200:
        print(f"❌ Failed to create quiz: {response.status_code}")
        return False
    
    print("✅ Successfully created quiz")
    
    # Now get the quiz list to find our newly created quiz
    quiz_list_url = "http://localhost:5000/teacher/course/COMP101/quiz"
    response = session.get(quiz_list_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to access quiz list: {response.status_code}")
        return False
    
    print("✅ Successfully accessed quiz list")
    
    # Parse the quiz list to find our quiz
    soup = BeautifulSoup(response.text, 'html.parser')
    quiz_links = soup.find_all('a', href=lambda href: href and '/quiz/' in href and '/edit' in href)
    
    if not quiz_links:
        print("❌ No quiz edit links found")
        return False
    
    # Get the first quiz ID
    href = quiz_links[0].get('href')
    parts = href.split('/')
    quiz_id = int(parts[5])
    
    print(f"✅ Found quiz ID: {quiz_id}")
    
    # Now try to edit the quiz
    edit_url = f"http://localhost:5000/teacher/course/COMP101/quiz/{quiz_id}/edit"
    response = session.get(edit_url)
    
    if response.status_code != 200:
        print(f"❌ Failed to access edit page: {response.status_code}")
        return False
    
    print("✅ Successfully accessed edit page")
    
    # Try to submit a simple edit
    edit_data = {
        'name': 'Test Quiz for Foreign Key Fix (Updated)',
        'description': 'This quiz has been updated to test the foreign key fix',
        'duration': '30',
        'attempt_limit': '3',
        'point_in_course': '10'
    }
    
    response = session.post(edit_url, data=edit_data)
    
    if response.status_code != 200:
        print(f"❌ Failed to update quiz: {response.status_code}")
        print("Response content:", response.text[:500])
        return False
    
    print("✅ Successfully updated quiz without foreign key errors")
    return True

if __name__ == "__main__":
    print("Testing quiz creation and editing...")
    success = test_create_and_edit_quiz()
    
    if success:
        print("\n✅ Quiz creation and edit test passed!")
    else:
        print("\n❌ Quiz creation and edit test failed!")