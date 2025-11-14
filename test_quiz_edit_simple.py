#!/usr/bin/env python3
"""
Simple test script to verify quiz editing works without foreign key violations
"""

import requests
import json

def test_quiz_edit_fix():
    """Test editing a quiz that has student responses"""
    
    # Create session
    session = requests.Session()
    
    # Login as teacher (john_smith teaches COMP101 and COMP201)
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
    
    # First, get the teacher quiz list to see available quizzes
    quiz_list_url = "http://localhost:5000/teacher/course/COMP201/quiz"
    response = session.get(quiz_list_url)
    
    if response.status_code == 200:
        print("✅ Successfully accessed teacher quiz list for COMP201")
        
        # Look for quiz IDs in the response
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find quiz IDs in the page
        quiz_links = soup.find_all('a', href=lambda href: href and '/quiz/' in href and '/edit' in href)
        quiz_ids = []
        for link in quiz_links:
            href = link.get('href', '')
            if '/quiz/' in href and '/edit' in href:
                # Extract quiz ID from URL like /teacher/course/COMP101/quiz/1/edit
                parts = href.split('/')
                if len(parts) >= 6:
                    try:
                        quiz_id = int(parts[5])
                        quiz_ids.append(quiz_id)
                    except ValueError:
                        pass
        
        if not quiz_ids:
            print("❌ No quiz IDs found in the quiz list")
            return False
            
        print(f"Found quiz IDs: {quiz_ids}")
        
        # Try to access the edit page for the first quiz
        quiz_id = quiz_ids[0]
        edit_url = f"http://localhost:5000/teacher/course/COMP201/quiz/{quiz_id}/edit"
        response = session.get(edit_url)
        
        if response.status_code == 200:
            print(f"✅ Successfully accessed edit page for Quiz {quiz_id}")
            
            # Try to submit a simple edit (just change the name)
            # Get current form data
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find form data
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
                print(f"✅ Successfully updated Quiz {quiz_id} in COMP201 without foreign key errors")
                return True
            else:
                print(f"❌ Failed to update Quiz {quiz_id}: {response.status_code}")
                print("Response content:", response.text[:500])
                return False
                
        else:
            print(f"❌ Failed to access edit page for Quiz {quiz_id}: {response.status_code}")
            print("Response content:", response.text[:500])
            return False
            
    else:
        print(f"❌ Failed to access teacher quiz list: {response.status_code}")
        print("Response content:", response.text[:500])
        return False

if __name__ == "__main__":
    print("Testing quiz edit functionality...")
    success = test_quiz_edit_fix()
    
    if success:
        print("\n✅ Quiz edit test passed!")
    else:
        print("\n❌ Quiz edit test failed!")