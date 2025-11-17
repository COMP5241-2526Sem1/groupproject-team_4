from app import app
from models import db, Quiz

with app.app_context():
    # Check quiz 5 details
    quiz5 = Quiz.query.filter_by(id=5).first()
    if quiz5:
        print(f"Quiz 5 details:")
        print(f"  Name: {quiz5.name}")
        print(f"  Course code: {quiz5.course_code}")
        print(f"  Attempt limit: {quiz5.attempt_limit}")
        
        # Check if user 'a' has used all attempts for quiz 5
        from models import User, Attempt
        user_a = User.query.filter_by(username='a').first()
        if user_a:
            attempts = Attempt.query.filter_by(quiz_id=5, user_id=user_a.id).count()
            print(f"  User 'a' attempts: {attempts}")
            print(f"  Can attempt: {attempts < (quiz5.attempt_limit or 999)}")
            
            # Test accessing quiz 5 with the correct course code
            import requests
            import json
            
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
            
            login_response = session.post(f"{BASE_URL}/login", data=json.dumps(login_data), headers=headers)
            if login_response.status_code == 200 and 'login success' in login_response.text:
                print("✅ Login successful!")
                
                # Access quiz 5 with correct course code
                quiz5_response = session.get(f"{BASE_URL}/course/{quiz5.course_code}/quiz/5")
                print(f"Quiz 5 access status: {quiz5_response.status_code}")
                
                if quiz5_response.status_code == 200:
                    import re
                    if 'View Results' in quiz5_response.text:
                        results_url_match = re.search(r'href=["\']([^"\']*results[^"\']*)["\']', quiz5_response.text, re.IGNORECASE)
                        if results_url_match:
                            href = results_url_match.group(1)
                            print(f"View Results URL: {href}")
                            if '/course//quiz/' in href:
                                print("❌ ISSUE: Empty course code found!")
                            else:
                                print("✅ Course code appears correctly")
                    else:
                        print("No View Results button found")
                        print("Saving HTML for inspection...")
                        with open('quiz5_no_view_results.html', 'w', encoding='utf-8') as f:
                            f.write(quiz5_response.text)
    else:
        print("Quiz 5 not found")