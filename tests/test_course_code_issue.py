import requests
import json

# Test with user 'a' to see if we can reproduce the empty course code issue
BASE_URL = "http://localhost:5000"

# Login as user 'a'
login_data = {
    'username': 'a',
    'password': 'comp5241',
    'role': 'student'
}

session = requests.Session()
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

print("🧪 Testing various scenarios to reproduce empty course code issue...")

# Login
login_response = session.post(f"{BASE_URL}/login", data=json.dumps(login_data), headers=headers)
if login_response.status_code == 200 and 'login success' in login_response.text:
    print("✅ Login successful!")
    
    # Test 1: Normal access to quiz 4 (COMP101)
    print("\n1. Testing normal quiz access...")
    quiz4_response = session.get(f"{BASE_URL}/course/COMP101/quiz/4")
    print(f"   Quiz 4 status: {quiz4_response.status_code}")
    
    if quiz4_response.status_code == 200:
        # Check if View Results button has correct URL
        if 'View Results' in quiz4_response.text:
            import re
            results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', quiz4_response.text, re.IGNORECASE)
            if results_url_match:
                href = results_url_match.group(1)
                print(f"   ✅ View Results URL: {href}")
                if '/course//quiz/' in href:
                    print(f"   ❌ ISSUE: Empty course code found in URL!")
                else:
                    print(f"   ✅ Course code appears correctly")
    
    # Test 2: Try accessing quiz with different course codes
    print("\n2. Testing edge cases...")
    
    # Try with non-existent course
    fake_response = session.get(f"{BASE_URL}/course/INVALID/quiz/4")
    print(f"   Invalid course status: {fake_response.status_code}")
    
    # Try with empty course code (if possible)
    try:
        empty_response = session.get(f"{BASE_URL}/course//quiz/4")
        print(f"   Empty course status: {empty_response.status_code}")
        if empty_response.status_code == 200:
            print("   ⚠️  Empty course code returned 200 - checking content...")
            if 'View Results' in empty_response.text:
                results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', empty_response.text, re.IGNORECASE)
                if results_url_match:
                    href = results_url_match.group(1)
                    print(f"   View Results URL with empty course: {href}")
    except Exception as e:
        print(f"   Empty course test failed: {e}")
    
    # Test 3: Check what happens with different quiz IDs
    print("\n3. Testing different quiz IDs...")
    for quiz_id in [1, 2, 3, 5, 6, 7]:
        try:
            quiz_response = session.get(f"{BASE_URL}/course/COMP101/quiz/{quiz_id}")
            print(f"   Quiz {quiz_id} status: {quiz_response.status_code}")
            
            if quiz_response.status_code == 200 and 'View Results' in quiz_response.text:
                results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', quiz_response.text, re.IGNORECASE)
                if results_url_match:
                    href = results_url_match.group(1)
                    if '/course//quiz/' in href:
                        print(f"   ❌ ISSUE: Empty course code in quiz {quiz_id}!")
                        print(f"      URL: {href}")
                        break
        except Exception as e:
            print(f"   Quiz {quiz_id} test failed: {e}")
            
else:
    print("❌ Login failed")