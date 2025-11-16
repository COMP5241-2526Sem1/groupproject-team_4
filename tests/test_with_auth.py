import requests
import json

# Base URL
base_url = "http://localhost:5000"

# Create a session to maintain cookies
session = requests.Session()

# First, let's try to login with user 'a' who we found completed Quiz 5
login_data = {
    "username": "a",
    "password": "a",  # Assuming password is same as username
    "role": "student"
}

print("Attempting to login...")
login_response = session.post(f"{base_url}/login", json=login_data)
print(f"Login status: {login_response.status_code}")
print(f"Login response: {login_response.text}")

if login_response.status_code == 200:
    print("Login successful!")
    
    # Now try to access the quiz page
    print("\nAccessing quiz page...")
    quiz_response = session.get(f"{base_url}/course/COMP101/quiz/5")
    print(f"Quiz page status: {quiz_response.status_code}")
    print(f"Quiz page URL: {quiz_response.url}")
    
    # Check if we got the actual quiz page or were redirected
    if "Sign In" in quiz_response.text:
        print("ERROR: Still redirected to login page!")
    else:
        print("SUCCESS: Accessed quiz page!")
        
        # Check for results preview elements
        if "Results Preview" in quiz_response.text:
            print("✓ Found 'Results Preview' in page")
        else:
            print("✗ 'Results Preview' not found in page")
            
        if "quiz-results" in quiz_response.text:
            print("✓ Found 'quiz-results' class in page")
        else:
            print("✗ 'quiz-results' class not found in page")
            
        # Save the response for inspection
        with open("quiz_page_response.html", "w", encoding="utf-8") as f:
            f.write(quiz_response.text)
        print("Response saved to quiz_page_response.html")
        
else:
    print("Login failed!")
    print("Trying with different credentials...")
    
    # Try with admin credentials
    login_data = {
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    }
    
    login_response = session.post(f"{base_url}/login", json=login_data)
    print(f"Admin login status: {login_response.status_code}")
    print(f"Admin login response: {login_response.text}")
    
    if login_response.status_code == 200:
        quiz_response = session.get(f"{base_url}/course/COMP101/quiz/5")
        print(f"Admin quiz page status: {quiz_response.status_code}")
        with open("admin_quiz_response.html", "w", encoding="utf-8") as f:
            f.write(quiz_response.text)
        print("Admin response saved to admin_quiz_response.html")