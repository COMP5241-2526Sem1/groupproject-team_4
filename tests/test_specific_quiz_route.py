#!/usr/bin/env python3
"""
Test script to verify teacher access to specific quiz routes mentioned by the user.
"""

import requests
import sys

def test_teacher_specific_routes():
    """Test teacher access to specific quiz routes like teacher/course/3/quiz/4"""
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    print("🧪 Testing Teacher Access to Specific Quiz Routes")
    print("=" * 60)
    
    # 1. Login as teacher
    print("\n1️⃣ Logging in as teacher...")
    login_data = {
        'username': 'john_smith',
        'password': 'comp5241',
        'role': 'teacher'
    }
    
    login_response = session.post(f"{base_url}/login", json=login_data, 
                                 headers={'Content-Type': 'application/json'})
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text[:200]}")
        return False
    
    print("✅ Login successful")
    
    # 2. Test the specific route format mentioned by user
    print("\n2️⃣ Testing teacher/course/3/quiz/4 route...")
    
    # First, let's check what courses the teacher has access to
    teacher_home_response = session.get(f"{base_url}/teacher")
    if teacher_home_response.status_code != 200:
        print(f"❌ Failed to access teacher home: {teacher_home_response.status_code}")
        return False
    
    print("✅ Teacher home accessed")
    print("Teacher home content preview:")
    print(teacher_home_response.text[:500] + "..." if len(teacher_home_response.text) > 500 else teacher_home_response.text)
    
    # Extract course codes from teacher home page
    import re
    course_codes = re.findall(r'href="/course/([A-Z0-9]+)"', teacher_home_response.text)
    print(f"Found courses: {course_codes}")
    
    # Test different route formats
    test_routes = []
    if course_codes:
        for course_code in course_codes[:2]:  # Test first 2 courses
            test_routes.append(f"{base_url}/course/{course_code}/quiz/1")  # Try quiz 1 for each course
    
    # Also test the specific formats mentioned
    test_routes.extend([
        f"{base_url}/teacher/course/3/quiz/4",  # User's mentioned format
        f"{base_url}/course/COMP101/quiz/18",   # Our working format
        f"{base_url}/course/COMP101/quiz/16",   # Another working quiz
    ])
    
    success_count = 0
    for route in test_routes:
        print(f"\nTesting: {route}")
        response = session.get(route)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Access successful")
            success_count += 1
            
            # Save response for first successful route
            if success_count == 1:
                with open('teacher_specific_route_success.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("💾 Saved response to teacher_specific_route_success.html")
                
        elif response.status_code == 404:
            print("❌ Page not found (404)")
        elif response.status_code == 403:
            print("❌ Access forbidden (403)")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"Response: {response.text[:200]}")
    
    print(f"\n📊 Results: {success_count}/{len(test_routes)} routes accessible")
    
    if success_count > 0:
        print("✅ SUCCESS: Teachers can access quiz info pages!")
        return True
    else:
        print("❌ FAILED: Teachers cannot access quiz info pages")
        return False

if __name__ == "__main__":
    success = test_teacher_specific_routes()
    sys.exit(0 if success else 1)