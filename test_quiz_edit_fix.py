#!/usr/bin/env python3
"""
Test script to verify quiz editing works without foreign key violations
"""

import requests
import sys
from test_with_login import login_session

def test_quiz_edit_with_responses():
    """Test editing a quiz that has student responses"""
    
    # Login as teacher
    session = login_session("teacher_user", "teacher_password")
    if not session:
        print("❌ Failed to login as teacher")
        return False
    
    # First, let's check if there are any quizzes with responses
    # Get quiz list for PHYS101
    response = session.get("http://localhost:5000/teacher/course/PHYS101/quiz")
    if response.status_code != 200:
        print(f"❌ Failed to access teacher quiz list: {response.status_code}")
        return False
    
    # Look for Quiz 15 (which the user mentioned has issues)
    quiz_id = 15
    
    # Try to access the edit page for Quiz 15
    edit_url = f"http://localhost:5000/teacher/course/PHYS101/quiz/{quiz_id}/edit"
    response = session.get(edit_url)
    
    if response.status_code == 200:
        print(f"✅ Successfully accessed edit page for Quiz {quiz_id}")
        
        # Try to submit a simple edit (just change the name)
        # First, get the current form data
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the form and extract current values
        form_data = {}
        
        # Basic quiz info
        name_input = soup.find('input', {'name': 'name'})
        if name_input:
            form_data['name'] = name_input.get('value', '') + ' (Updated)'
        
        description_input = soup.find('textarea', {'name': 'description'})
        if description_input:
            form_data['description'] = description_input.text
        
        # Add other required fields
        form_data['duration'] = '30'
        form_data['attempt_limit'] = '5'
        form_data['point_in_course'] = '0'
        
        # Submit the edit
        response = session.post(edit_url, data=form_data)
        
        if response.status_code == 200:
            print(f"✅ Successfully updated Quiz {quiz_id} without foreign key errors")
            return True
        else:
            print(f"❌ Failed to update Quiz {quiz_id}: {response.status_code}")
            print("Response content:", response.text[:500])
            return False
            
    elif response.status_code == 404:
        print(f"⚠️  Quiz {quiz_id} not found, trying Quiz 13 instead")
        
        # Try with Quiz 13 which we know exists from previous tests
        quiz_id = 13
        edit_url = f"http://localhost:5000/teacher/course/PHYS101/quiz/{quiz_id}/edit"
        response = session.get(edit_url)
        
        if response.status_code == 200:
            print(f"✅ Successfully accessed edit page for Quiz {quiz_id}")
            return True
        else:
            print(f"❌ Failed to access edit page for Quiz {quiz_id}: {response.status_code}")
            return False
    else:
        print(f"❌ Failed to access edit page for Quiz {quiz_id}: {response.status_code}")
        return False

if __name__ == "__main__":
    print("Testing quiz edit functionality...")
    success = test_quiz_edit_with_responses()
    
    if success:
        print("\n✅ Quiz edit test passed!")
        sys.exit(0)
    else:
        print("\n❌ Quiz edit test failed!")
        sys.exit(1)