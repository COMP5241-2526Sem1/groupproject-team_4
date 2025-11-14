import requests
import sys
from app import app
from models import db, User, Course, Quiz, CourseEnrollment, Submission

def test_quiz_results_access():
    """Test accessing quiz results page to reproduce the 404 error"""
    
    with app.app_context():
        # Use Quiz ID 4 (COMP101) which has submissions
        quiz_id = 4
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            print(f"Quiz {quiz_id} not found")
            return
            
        course_code = quiz.course_code
        print(f"Testing quiz results for Quiz {quiz_id} ({quiz.name}) in course {course_code}")
        
        # Find a student who has submissions for this quiz
        submissions = Submission.query.filter_by(quiz_id=quiz_id).all()
        if not submissions:
            print(f"No submissions found for quiz {quiz_id}")
            return
            
        student = User.query.get(submissions[0].user_id)
        if not student:
            print(f"Student not found")
            return
            
        print(f"Using student: {student.username}")
        
        # Check enrollment
        enrollment = CourseEnrollment.query.filter_by(
            student_id=student.id, 
            course_code=course_code
        ).first()
        
        if not enrollment:
            print(f"Student {student.username} is not enrolled in {course_code}")
            return
            
        print(f"Student is enrolled: Yes")
        
        # Expected URL
        expected_url = f"http://localhost:5000/course/{course_code}/quiz/{quiz_id}/results"
        print(f"Expected URL: {expected_url}")
        
        # Try to access the quiz info page first to see the View Results button
        quiz_info_url = f"http://localhost:5000/course/{course_code}/quiz/{quiz_id}"
        print(f"Quiz info URL: {quiz_info_url}")
        
        # Test with session (simulate logged in user)
        session = requests.Session()
        
        # First, try to login
        login_data = {
            'username': student.username,
            'password': 'password123'  # Try common password
        }
        
        print("Attempting login...")
        try:
            login_response = session.post('http://localhost:5000/login', data=login_data)
            print(f"Login response status: {login_response.status_code}")
            if login_response.status_code == 200:
                print("Login successful")
                
                # Now try to access quiz info page
                print("Accessing quiz info page...")
                quiz_info_response = session.get(quiz_info_url)
                print(f"Quiz info response status: {quiz_info_response.status_code}")
                
                if quiz_info_response.status_code == 200:
                    content = quiz_info_response.text
                    
                    # Look for the View Results button URL
                    if 'View Results' in content:
                        print("Found 'View Results' button in response")
                        
                        # Look for the URL pattern
                        import re
                        url_pattern = r'/course/([^/]*)/quiz/(\d+)/results'
                        matches = re.findall(url_pattern, content)
                        
                        if matches:
                            print("Found View Results URLs:")
                            for match in matches:
                                course_code_found, quiz_id_found = match
                                print(f"  Course: '{course_code_found}', Quiz: {quiz_id_found}")
                                if not course_code_found:
                                    print("  WARNING: Empty course code found!")
                        else:
                            print("No View Results URLs found in content")
                    else:
                        print("No 'View Results' button found in response")
                        
                    # Save response for debugging
                    with open('quiz_info_response.html', 'w', encoding='utf-8') as f:
                        f.write(content)
                    print("Saved quiz info response to quiz_info_response.html")
                    
                else:
                    print(f"Failed to access quiz info: {quiz_info_response.status_code}")
                    
            else:
                print("Login failed")
                
        except Exception as e:
            print(f"Error during test: {e}")

if __name__ == "__main__":
    test_quiz_results_access()