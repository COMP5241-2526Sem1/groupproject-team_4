import requests
import json

# Base URL
base_url = "http://localhost:5000"

# Create a session to maintain cookies
session = requests.Session()

# Common password patterns to try
passwords_to_try = ["a", "password", "password123", "123456", "admin"]

print("Testing login for user 'a'...")

for password in passwords_to_try:
    print(f"\nTrying password: {password}")
    login_data = {
        "username": "a",
        "password": password,
        "role": "student"
    }
    
    login_response = session.post(f"{base_url}/login", json=login_data)
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        print(f"SUCCESS! Password is: {password}")
        print(f"Login response: {login_response.text}")
        
        # Test accessing quiz page
        quiz_response = session.get(f"{base_url}/course/COMP101/quiz/5")
        print(f"Quiz page status: {quiz_response.status_code}")
        print(f"Quiz page URL: {quiz_response.url}")
        
        if "Sign In" not in quiz_response.text:
            print("SUCCESS: Accessed quiz page!")
            
            # Check for results preview
            if "Results Preview" in quiz_response.text:
                print("✓ Found 'Results Preview' in page")
            else:
                print("✗ 'Results Preview' not found in page")
                
            # Save response
            with open("user_a_quiz_response.html", "w", encoding="utf-8") as f:
                f.write(quiz_response.text)
            print("Response saved to user_a_quiz_response.html")
            break
        else:
            print("Still redirected to login")
            
    else:
        print(f"Failed with password: {password}")

# Also try with student alice_johnson
print("\n\nTesting with alice_johnson...")
for password in ["alice", "password", "123456"]:
    login_data = {
        "username": "alice_johnson",
        "password": password,
        "role": "student"
    }
    
    login_response = session.post(f"{base_url}/login", json=login_data)
    if login_response.status_code == 200:
        print(f"SUCCESS! alice_johnson password is: {password}")
        break