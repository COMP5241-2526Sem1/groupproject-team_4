import requests
import json
import re

# Let's test a specific scenario that might cause empty course code
# Maybe the issue occurs when accessing quiz results directly without going through the quiz info page

BASE_URL = "http://localhost:5000"
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

print("🧪 Testing direct access to quiz results...")

# Login
login_response = session.post(f"{BASE_URL}/login", data=json.dumps(login_data), headers=headers)
if login_response.status_code == 200 and 'login success' in login_response.text:
    print("✅ Login successful!")
    
    # Test 1: Direct access to results page
    print("\n1. Testing direct access to quiz results...")
    results_response = session.get(f"{BASE_URL}/course/COMP101/quiz/4/results")
    print(f"   Direct results access status: {results_response.status_code}")
    
    if results_response.status_code == 200:
        # Check for any links or buttons that might have empty course code
        all_hrefs = re.findall(r'href=["\']([^"\']*)["\']', results_response.text, re.IGNORECASE)
        print(f"   Found {len(all_hrefs)} href links:")
        for href in all_hrefs[:10]:  # Show first 10
            if '/course//quiz/' in href:
                print(f"   ❌ ISSUE: Empty course code in href: {href}")
            elif 'course' in href:
                print(f"   ✅ Course link: {href}")
    
    # Test 2: Check if there's a different way to access quiz info that might cause issues
    print("\n2. Testing different access patterns...")
    
    # Try accessing quiz list first, then quiz info
    quiz_list_response = session.get(f"{BASE_URL}/course/COMP101/quiz")
    print(f"   Quiz list status: {quiz_list_response.status_code}")
    
    if quiz_list_response.status_code == 200:
        # Look for quiz 4 link
        quiz4_link_match = re.search(r'href=["\']([^"\']*quiz/4[^"\']*)["\']', quiz_list_response.text, re.IGNORECASE)
        if quiz4_link_match:
            quiz4_link = quiz4_link_match.group(1)
            print(f"   Quiz 4 link from list: {quiz4_link}")
            
            # Access quiz 4 through this link
            quiz4_via_list = session.get(f"{BASE_URL}{quiz4_link}")
            print(f"   Quiz 4 via list status: {quiz4_via_list.status_code}")
            
            if quiz4_via_list.status_code == 200 and 'View Results' in quiz4_via_list.text:
                results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', quiz4_via_list.text, re.IGNORECASE)
                if results_url_match:
                    href = results_url_match.group(1)
                    print(f"   View Results URL via list: {href}")
                    if '/course//quiz/' in href:
                        print("❌ ISSUE: Empty course code found when accessing via list!")
    
    # Test 3: Check if issue occurs with different courses
    print("\n3. Testing different courses...")
    
    # Let's check what other courses exist
    from app import app
    from models import Course, CourseEnrollment, User
    
    with app.app_context():
        user_a = User.query.filter_by(username='a').first()
        if user_a:
            # Get user's enrolled courses
            enrollments = CourseEnrollment.query.filter_by(student_id=user_a.id).all()
            print(f"   User 'a' enrolled in {len(enrollments)} courses:")
            
            for enrollment in enrollments:
                course = Course.query.get(enrollment.course_code)
                if course:
                    print(f"   - {course.code}: {course.name}")
                    
                    # Test accessing a quiz in this course
                    from models import Quiz
                    quizzes = Quiz.query.filter_by(course_code=course.code).all()
                    if quizzes:
                        quiz = quizzes[0]  # Test first quiz
                        print(f"     Testing quiz {quiz.id}...")
                        
                        quiz_response = session.get(f"{BASE_URL}/course/{course.code}/quiz/{quiz.id}")
                        print(f"     Quiz {quiz.id} status: {quiz_response.status_code}")
                        
                        if quiz_response.status_code == 200 and 'View Results' in quiz_response.text:
                            results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', quiz_response.text, re.IGNORECASE)
                            if results_url_match:
                                href = results_url_match.group(1)
                                if '/course//quiz/' in href:
                                    print(f"     ❌ ISSUE: Empty course code in {course.code} quiz {quiz.id}!")
                                    print(f"        URL: {href}")
                                else:
                                    print(f"     ✅ Course code appears correctly")
else:
    print("❌ Login failed")