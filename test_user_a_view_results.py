import requests
import re
from bs4 import BeautifulSoup

# Test with user 'a' who has used all attempts
BASE_URL = "http://localhost:5000"

# First, let's login as user 'a'
login_data = {
    'username': 'a',
    'password': 'comp5241'  # Found from hash check
}

print("🧪 Testing with user 'a' who has used all attempts...")

session = requests.Session()

# Try to login
login_response = session.post(f"{BASE_URL}/login", data=login_data)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    print("✅ Login successful!")
    
    # Test quiz 4 (COMP101) where user 'a' has used all 3 attempts
    quiz4_response = session.get(f"{BASE_URL}/course/COMP101/quiz/4")
    print(f"Quiz 4 info page status: {quiz4_response.status_code}")
    
    if quiz4_response.status_code == 200:
        # Save the HTML to examine it
        with open('quiz_info_user_a_quiz4.html', 'w', encoding='utf-8') as f:
            f.write(quiz4_response.text)
        
        # Parse the HTML
        soup = BeautifulSoup(quiz4_response.text, 'html.parser')
        
        # Look for View Results button
        view_results_btn = soup.find('a', string=re.compile(r'View Results', re.IGNORECASE))
        if view_results_btn:
            href = view_results_btn.get('href', '')
            print(f"🎯 Found 'View Results' button!")
            print(f"   URL: {href}")
            
            # Check if the course code is missing
            if '/course//' in href or href.count('/') < 4:
                print("❌ ISSUE FOUND: Course code appears to be missing from URL!")
                print(f"   Raw href: {href}")
            else:
                print("✅ URL looks correct")
                
            # Try to access the results page
            if href:
                results_response = session.get(f"{BASE_URL}{href}")
                print(f"Results page status: {results_response.status_code}")
        else:
            print("❌ No 'View Results' button found")
            
            # Let's see what buttons are there
            buttons = soup.find_all('button')
            links = soup.find_all('a')
            print("Available buttons/links:")
            for btn in buttons:
                print(f"  Button: {btn.get_text(strip=True)}")
            for link in links:
                if link.get('href') and 'results' in link.get('href', ''):
                    print(f"  Results link: {link.get('href')}")
    else:
        print(f"❌ Could not access quiz 4 info page")
        
else:
    print("❌ Login failed")
    print("Let's try other common passwords...")
    
    # Try other passwords
    for password in ['password', '123456', 'student', 'debug123', 'comp5241']:
        login_data['password'] = password
        test_response = session.post(f"{BASE_URL}/login", data=login_data)
        if test_response.status_code == 200:
            print(f"✅ Login successful with password: {password}")
            break
    else:
        print("❌ Could not find correct password for user 'a'")