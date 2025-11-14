import requests
import re

def test_quiz_info_page():
    """Test accessing quiz info page to see the rendered HTML"""
    
    # Test URL for quiz 4 in COMP101
    url = "http://localhost:5000/course/COMP101/quiz/4"
    
    try:
        # First, let's try to access without login to see what happens
        print("Testing quiz info page without login...")
        response = requests.get(url, allow_redirects=True)
        print(f"Status code: {response.status_code}")
        print(f"Final URL: {response.url}")
        
        if response.status_code == 200:
            content = response.text
            
            # Look for the View Results button and its URL
            if 'View Results' in content:
                print("Found 'View Results' button")
                
                # Find the onclick handler
                onclick_pattern = r'onclick="window\.location\.href=\'(/course/[^/]*)/quiz/(\d+)/results)\'"'
                matches = re.findall(onclick_pattern, content)
                
                if matches:
                    print("Found View Results URLs:")
                    for match in matches:
                        full_url, course_part, quiz_part = match
                        print(f"  Full URL: '{full_url}'")
                        print(f"  Course part: '{course_part}'")
                        if not course_part or course_part.strip() == '':
                            print("  WARNING: Empty or whitespace course code!")
                else:
                    # Try broader pattern
                    broader_pattern = r'/course/([^/]*)/quiz/(\d+)/results'
                    matches = re.findall(broader_pattern, content)
                    if matches:
                        print("Found quiz results URLs:")
                        for course_code_found, quiz_id_found in matches:
                            print(f"  Course: '{course_code_found}', Quiz: {quiz_id_found}")
                            if not course_code_found or course_code_found.strip() == '':
                                print("  WARNING: Empty or whitespace course code!")
                    else:
                        print("No quiz results URLs found")
                        
                # Save the response for debugging
                with open('quiz_info_debug.html', 'w', encoding='utf-8') as f:
                    f.write(content)
                print("Saved response to quiz_info_debug.html")
                
            else:
                print("No 'View Results' button found")
                
        else:
            print(f"Failed to access page: {response.status_code}")
            print(f"Response content preview: {response.text[:500]}...")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_quiz_info_page()