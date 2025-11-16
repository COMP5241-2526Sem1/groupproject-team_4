#!/usr/bin/env python3
"""
Simple test to verify login and course_code fixes work.
"""

import requests
import re

def test_login_and_course_code_fixes():
    """Test login and check for course_code issues"""
    
    # Test login page first
    print("Testing login page...")
    try:
        response = requests.get('http://localhost:5000/login', timeout=10)
        if response.status_code == 200:
            print("✅ Login page is accessible")
        else:
            print(f"❌ Login page returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to access login page: {e}")
        return False
    
    # Test login
    print("Testing login...")
    session = requests.Session()
    
    # Get login page to extract CSRF token if needed
    login_page = session.get('http://localhost:5000/login')
    
    # Try login with form data
    login_data = {
        'username': 'a',
        'password': 'a',
        'role': 'student'
    }
    
    try:
        login_response = session.post('http://localhost:5000/login', data=login_data, timeout=10)
        print(f"Login response status: {login_response.status_code}")
        
        # Check if login was successful by looking at the response
        if 'Login' in login_response.text or 'username' in login_response.text:
            print("❌ Login appears to have failed - still showing login page")
            return False
        else:
            print("✅ Login appears successful")
    
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False
    
    # Test course pages for course_code issues
    print("\nTesting course pages for course_code issues...")
    
    # Test quiz list page
    try:
        response = session.get('http://localhost:5000/course/COMP101/quiz/', timeout=10)
        print(f"Quiz list status: {response.status_code}")
        
        if '/course//quiz/' in response.text:
            print("❌ Found empty course_code in quiz list")
            return False
        else:
            print("✅ No empty course_code found in quiz list")
            
        # Look for View Results buttons and test them
        results_links = re.findall(r'href="(/course/COMP101/quiz/\d+/results)"', response.text)
        print(f"Found {len(results_links)} results links")
        
        for link in results_links[:1]:  # Test first results link
            print(f"Testing results link: {link}")
            results_response = session.get(f'http://localhost:5000{link}', timeout=10)
            print(f"Results status: {results_response.status_code}")
            
            if '/course//quiz/' in results_response.text:
                print(f"❌ Found empty course_code in results page")
                return False
            else:
                print(f"✅ No empty course_code found in results page")
                
    except Exception as e:
        print(f"❌ Error testing course pages: {e}")
        return False
    
    # Test non-existent quiz
    print("\nTesting non-existent quiz...")
    try:
        response = session.get('http://localhost:5000/course/COMP101/quiz/999', timeout=10)
        print(f"Non-existent quiz status: {response.status_code}")
        
        if '/course//quiz/' in response.text:
            print("❌ Found empty course_code in non-existent quiz page")
            return False
        else:
            print("✅ No empty course_code found in non-existent quiz page")
    except Exception as e:
        print(f"❌ Error testing non-existent quiz: {e}")
        return False
    
    print("\n🎉 All tests passed! Course code fixes are working.")
    return True

if __name__ == "__main__":
    print("Testing login and course code fixes...")
    print("=" * 50)
    
    success = test_login_and_course_code_fixes()
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed.")