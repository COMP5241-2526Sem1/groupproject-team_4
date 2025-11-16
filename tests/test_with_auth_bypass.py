#!/usr/bin/env python3
"""
Test script to verify Add Question functionality with authentication bypass
"""

import requests
import re
from urllib.parse import urljoin

def test_with_auth_bypass():
    """Test the quiz edit page functionality by simulating an authenticated session"""
    
    print("🔍 Testing Add Question functionality with authentication bypass...")
    
    # Base URL
    base_url = "http://127.0.0.1:5000"
    
    # Test the actual quiz edit page
    quiz_edit_url = f"{base_url}/teacher/course/CS101/quiz/1/edit"
    
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # First, try to access the login page to get session cookies
        login_url = f"{base_url}/login"
        print(f"📋 Accessing login page: {login_url}")
        
        login_response = session.get(login_url)
        print(f"Login page status: {login_response.status_code}")
        
        # Try to access the quiz edit page directly
        print(f"📝 Accessing quiz edit page: {quiz_edit_url}")
        response = session.get(quiz_edit_url, allow_redirects=True)
        
        print(f"Response status: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        # Check if we got redirected to login
        if 'login' in response.url.lower():
            print("🔒 Authentication required - redirected to login page")
            
            # Check the HTML content to see what's happening
            if response.text:
                if 'sign' in response.text.lower() or 'login' in response.text.lower():
                    print("📄 Page shows sign-in form")
                
                # Look for the Add Question button in the response
                if 'add-question-btn' in response.text:
                    print("✅ Add Question button found in HTML")
                else:
                    print("❌ Add Question button NOT found in HTML")
                
                # Check for JavaScript functions
                if 'addQuestion' in response.text:
                    print("✅ addQuestion function found in JavaScript")
                else:
                    print("❌ addQuestion function NOT found in JavaScript")
                
                # Check for questions container
                if 'questions-container' in response.text:
                    print("✅ Questions container found in HTML")
                else:
                    print("❌ Questions container NOT found in HTML")
            
            print("\n🔧 Recommendations:")
            print("1. The authentication system is working correctly")
            print("2. To test the Add Question functionality, you need to:")
            print("   - Log in as a teacher user")
            print("   - Navigate to the quiz edit page")
            print("   - Or create a test account with teacher privileges")
            
        else:
            print("🎉 Successfully accessed quiz edit page!")
            
            # Check for the Add Question button
            if 'add-question-btn' in response.text:
                print("✅ Add Question button found in HTML")
            else:
                print("❌ Add Question button NOT found in HTML")
            
            # Check for JavaScript functions
            if 'addQuestion' in response.text:
                print("✅ addQuestion function found in JavaScript")
            else:
                print("❌ addQuestion function NOT found in JavaScript")
            
            # Check for questions container
            if 'questions-container' in response.text:
                print("✅ Questions container found in HTML")
            else:
                print("❌ Questions container NOT found in HTML")
        
        # Test the standalone functionality page
        test_url = f"{base_url}/test_javascript_functionality.html"
        print(f"\n🧪 Testing standalone functionality: {test_url}")
        
        test_response = session.get(test_url)
        print(f"Test page status: {test_response.status_code}")
        
        if test_response.status_code == 200:
            print("✅ Test page is accessible")
            
            # Check for key elements in the test page
            if 'addQuestion' in test_response.text:
                print("✅ addQuestion function found in test page")
            
            if 'add-question-btn' in test_response.text:
                print("✅ Add Question button found in test page")
            
            print("\n🎯 Next Steps:")
            print("1. Open the test page in your browser: http://localhost:8080/test_javascript_functionality.html")
            print("2. Click 'Run All Tests' to verify the JavaScript functionality works")
            print("3. If the test page works, the issue is likely authentication-related")
            print("4. To fix the actual page, ensure you're logged in as a teacher")
            
        else:
            print("❌ Test page not accessible")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the Flask server")
        print("Make sure the server is running with: python app.py")
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    test_with_auth_bypass()