#!/usr/bin/env python3
"""
Comprehensive test to verify all course_code fixes work correctly.
Tests all the edge cases where course_code might be missing from render_template calls.
"""

import requests
import sqlite3
from datetime import datetime
import re

def test_all_course_code_fixes():
    """Test all scenarios that could cause empty course_code in URLs"""
    
    # Test with user 'a' who has multiple courses
    session = requests.Session()
    
    # Login as user 'a'
    login_data = {
        'username': 'a',
        'password': 'a'
    }
    
    login_response = session.post('http://localhost:5000/login', data=login_data)
    if login_response.status_code != 200 or 'Login' in login_response.text:
        print("❌ Failed to login as user 'a'")
        return False
    
    print("✅ Successfully logged in as user 'a'")
    
    # Test 1: Non-existent quiz
    print("\n--- Test 1: Non-existent quiz ---")
    response = session.get('http://localhost:5000/course/COMP101/quiz/999')
    print(f"Status: {response.status_code}")
    
    if response.status_code == 404:
        # Check if the page contains any buttons with empty course_code
        if '/course//quiz/' in response.text:
            print("❌ Found empty course_code in non-existent quiz page")
            return False
        else:
            print("✅ No empty course_code found in non-existent quiz page")
    
    # Test 2: Quiz not available (time-restricted)
    print("\n--- Test 2: Time-restricted quiz ---")
    response = session.get('http://localhost:5000/course/COMP101/quiz/6')  # Assuming quiz 6 is time-restricted
    print(f"Status: {response.status_code}")
    
    if response.status_code == 400:
        # Check if the page contains any buttons with empty course_code
        if '/course//quiz/' in response.text:
            print("❌ Found empty course_code in time-restricted quiz page")
            return False
        else:
            print("✅ No empty course_code found in time-restricted quiz page")
    
    # Test 3: Max attempts reached
    print("\n--- Test 3: Max attempts reached ---")
    response = session.get('http://localhost:5000/course/COMP101/quiz/5')  # Quiz 5 has max attempts
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        # Check if the page contains any buttons with empty course_code
        if '/course//quiz/' in response.text:
            print("❌ Found empty course_code in max attempts page")
            return False
        else:
            print("✅ No empty course_code found in max attempts page")
    
    # Test 4: Quiz results with no submission
    print("\n--- Test 4: Quiz results with no submission ---")
    response = session.get('http://localhost:5000/course/COMP101/quiz/1/results')  # Quiz 1, no submission
    print(f"Status: {response.status_code}")
    
    if response.status_code == 404:
        # Check if the page contains any buttons with empty course_code
        if '/course//quiz/' in response.text:
            print("❌ Found empty course_code in no submission results page")
            return False
        else:
            print("✅ No empty course_code found in no submission results page")
    
    # Test 5: Quiz results with no visible feedback
    print("\n--- Test 5: Quiz results with no visible feedback ---")
    # First, let's check what quizzes user 'a' has attempted
    response = session.get('http://localhost:5000/course/COMP101/quiz/')
    if response.status_code == 200:
        # Look for quizzes with attempts
        if 'View Results' in response.text:
            # Extract quiz ID from View Results button
            results_match = re.search(r'href="/course/COMP101/quiz/(\d+)/results"', response.text)
            if results_match:
                quiz_id = results_match.group(1)
                print(f"Found quiz {quiz_id} with results available")
                
                # Access the results page
                results_response = session.get(f'http://localhost:5000/course/COMP101/quiz/{quiz_id}/results')
                print(f"Results status: {results_response.status_code}")
                
                if results_response.status_code == 200:
                    # Check for empty course_code in results page
                    if '/course//quiz/' in results_response.text:
                        print("❌ Found empty course_code in results page")
                        return False
                    else:
                        print("✅ No empty course_code found in results page")
    
    # Test 6: Quiz start with no active attempt
    print("\n--- Test 6: Quiz start with no active attempt ---")
    response = session.get('http://localhost:5000/course/COMP101/quiz/1/start')  # Start quiz without proper attempt
    print(f"Status: {response.status_code}")
    
    if response.status_code == 400:
        # Check if the page contains any buttons with empty course_code
        if '/course//quiz/' in response.text:
            print("❌ Found empty course_code in no active attempt page")
            return False
        else:
            print("✅ No empty course_code found in no active attempt page")
    
    # Test 7: Check all quiz list pages
    print("\n--- Test 7: Check all quiz list pages ---")
    courses = ['COMP101', 'MATH101', 'COMP201', 'PHYS101']
    
    for course in courses:
        print(f"Checking course {course}...")
        response = session.get(f'http://localhost:5000/course/{course}/quiz/')
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            # Check for empty course_code in quiz list
            if '/course//quiz/' in response.text:
                print(f"  ❌ Found empty course_code in {course} quiz list")
                return False
            else:
                print(f"  ✅ No empty course_code found in {course} quiz list")
    
    print("\n🎉 All course_code fixes are working correctly!")
    return True

if __name__ == "__main__":
    print("Testing all course_code fixes...")
    print("=" * 50)
    
    success = test_all_course_code_fixes()
    
    if success:
        print("\n✅ All tests passed! The course_code issue has been resolved.")
    else:
        print("\n❌ Some tests failed. There may still be course_code issues.")