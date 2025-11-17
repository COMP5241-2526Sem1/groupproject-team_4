import requests
import re

# Test with user 'a' who has used all attempts
BASE_URL = "http://localhost:5000"

# First, let's login as user 'a'
login_data = {
    'username': 'a',
    'password': 'comp5241',
    'role': 'student'
}

print("🧪 Testing with user 'a' who has used all attempts...")

session = requests.Session()

# Try to login with JSON format
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

import json
login_response = session.post(f"{BASE_URL}/login", data=json.dumps(login_data), headers=headers)
print(f"Login status: {login_response.status_code}")
print(f"Login response URL: {login_response.url}")

if login_response.status_code == 200 and 'login success' in login_response.text:
    print("✅ Login successful!")
    
    # Test quiz 4 (COMP101) where user 'a' has used all 3 attempts
    quiz4_response = session.get(f"{BASE_URL}/course/COMP101/quiz/4")
    print(f"Quiz 4 info page status: {quiz4_response.status_code}")
    
    if quiz4_response.status_code == 200:
        # Save the HTML to examine it
        with open('quiz_info_user_a_quiz4.html', 'w', encoding='utf-8') as f:
            f.write(quiz4_response.text)
        
        # Look for View Results button using simple string search
        html_content = quiz4_response.text
        
        if 'View Results' in html_content:
            print("🎯 Found 'View Results' button!")
            
            # Find the URL using regex
            results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', html_content, re.IGNORECASE)
            if results_url_match:
                href = results_url_match.group(1)
                print(f"   URL: {href}")
                
                # Check if the course code is missing
                if '/course//' in href or '/course//quiz/' in href:
                    print("❌ ISSUE FOUND: Course code appears to be missing from URL!")
                    print(f"   Raw href: {href}")
                else:
                    print("✅ URL looks correct")
                    
                # Try to access the results page
                results_response = session.get(f"{BASE_URL}{href}")
                print(f"Results page status: {results_response.status_code}")
            else:
                print("❌ Could not extract results URL with regex")
        else:
            print("❌ No 'View Results' button found")
            
            # Let's see what buttons are there
            if 'Start Quiz' in html_content:
                print("  Found 'Start Quiz' button instead")
            if 'Back to List' in html_content:
                print("  Found 'Back to List' button")
                
            # Save HTML for manual inspection
            print("HTML saved to quiz_info_user_a_quiz4.html for inspection")
    else:
        print(f"❌ Could not access quiz 4 info page")
        
else:
    print("❌ Login failed")
    print("Response content:", login_response.text[:200])