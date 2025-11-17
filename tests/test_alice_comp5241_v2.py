import requests
import json
import re

def test_with_alice_comp5241():
    """Test quiz info page with alice_johnson login using correct password"""
    
    # Login first
    login_url = "http://localhost:5000/login"
    login_data = {
        "username": "alice_johnson",
        "password": "comp5241",  # Found this from the hash
        "role": "student"
    }
    
    session = requests.Session()
    
    print("Attempting login as alice_johnson with password comp5241...")
    login_response = session.post(login_url, json=login_data)
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        print("Login successful!")
        login_result = login_response.json()
        print(f"Login response: {login_result}")
        
        # Now test quiz info page for quiz 4 (COMP101) - alice has submissions here
        quiz_info_url = "http://localhost:5000/course/COMP101/quiz/4"
        print(f"Accessing quiz info page: {quiz_info_url}")
        
        quiz_response = session.get(quiz_info_url)
        print(f"Quiz info status: {quiz_response.status_code}")
        
        if quiz_response.status_code == 200:
            content = quiz_response.text
            
            # Look for View Results button
            if 'View Results' in content:
                print("✅ Found 'View Results' button")
                
                # Find the onclick handlers
                onclick_pattern = r'onclick="window\.location\.href=\'(/course/[^/]*)/quiz/(\d+)/results\'"'
                matches = re.findall(onclick_pattern, content)
                
                if matches:
                    print("Found View Results URLs:")
                    for match in matches:
                        full_url, course_part, quiz_part = match
                        print(f"  Full URL: '{full_url}'")
                        print(f"  Course part: '{course_part}'")
                        if not course_part or course_part.strip() == '':
                            print("  ⚠️  WARNING: Empty or whitespace course code!")
                else:
                    # Try broader pattern
                    broader_pattern = r'/course/([^/]*)/quiz/(\d+)/results'
                    matches = re.findall(broader_pattern, content)
                    if matches:
                        print("Found quiz results URLs:")
                        for course_code_found, quiz_id_found in matches:
                            print(f"  Course: '{course_code_found}', Quiz: {quiz_id_found}")
                            if not course_code_found or course_code_found.strip() == '':
                                print("  ⚠️  WARNING: Empty or whitespace course code!")
                    else:
                        print("No quiz results URLs found")
                        
                # Save the response for debugging
                with open('quiz_info_alice_comp5241.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("💾 Saved response to quiz_info_alice_comp5241.html")
                
                # Now try to access the results page directly
                results_url = "http://localhost:5000/course/COMP101/quiz/4/results"
                print(f"Testing results page: {results_url}")
                results_response = session.get(results_url)
                print(f"Results page status: {results_response.status_code}")
                
                if results_response.status_code == 404:
                    print("❌ Got 404 on results page - this is the issue!")
                    print(f"Results page content: {results_response.text[:500]}...")
                else:
                    print("✅ Results page accessible")
                    
            else:
                print("❌ No 'View Results' button found")
                print("Looking for other patterns...")
                
                # Check if there are any buttons or links
                if 'results' in content.lower():
                    print("Found 'results' text in content")
                    
                if 'button' in content.lower():
                    print("Found button elements")
                    
                # Look for any course/quiz patterns
                course_quiz_pattern = r'/course/[^/]*/quiz/\d+'
                matches = re.findall(course_quiz_pattern, content)
                if matches:
                    print("Found course/quiz URLs:")
                    for url in matches:
                        print(f"  {url}")
                        
                # Save the full response for debugging
                with open('quiz_info_alice_comp5241.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("💾 Saved full response to quiz_info_alice_comp5241.html")
                
        else:
            print(f"Failed to access quiz info: {quiz_response.status_code}")
            print(f"Response: {quiz_response.text[:500]}...")
            
    else:
        print("Login failed")
        print(f"Response: {login_response.text}")

if __name__ == "__main__":
    test_with_alice_comp5241()