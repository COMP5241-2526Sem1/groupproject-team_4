#!/usr/bin/env python3
"""
Debug script to see what's in the quiz list page
"""

import requests
import json

def debug_quiz_list():
    """Debug the quiz list page"""
    
    # Create session
    session = requests.Session()
    
    # Login as teacher
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
    
    # Get the teacher quiz list
    quiz_list_url = "http://localhost:5000/teacher/course/COMP101/quiz"
    response = session.get(quiz_list_url)
    
    if response.status_code == 200:
        print("✅ Successfully accessed teacher quiz list for COMP101")
        print("Response length:", len(response.text))
        print("\nFirst 1000 characters of response:")
        print(response.text[:1000])
        print("\n" + "="*50)
        print("Looking for quiz-related content...")
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for all links
        all_links = soup.find_all('a')
        print(f"\nFound {len(all_links)} links total:")
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            print(f"  Link: {href} - Text: {text}")
        
        # Look for quiz-specific patterns
        quiz_patterns = soup.find_all(text=lambda text: text and 'quiz' in text.lower())
        print(f"\nFound {len(quiz_patterns)} text elements containing 'quiz':")
        for pattern in quiz_patterns:
            print(f"  Text: {pattern.strip()}")
            
    else:
        print(f"❌ Failed to access teacher quiz list: {response.status_code}")
        print("Response content:", response.text[:500])
        return False

if __name__ == "__main__":
    debug_quiz_list()