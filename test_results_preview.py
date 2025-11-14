import requests
import sys

def test_quiz_info_page():
    """Test the quiz info page to see if results preview is displayed"""
    
    # Test cookies for student 31
    cookies = {'session_id': 'student31_session'}
    
    try:
        # Test quiz 4 (Python Basics Quiz) - should show results preview
        print("Testing Quiz 4 (Python Basics Quiz)...")
        response = requests.get('http://localhost:5000/course/COMP101/quiz/4', cookies=cookies, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        
        # Check if we can see results preview content
        if 'Your Results Preview' in response.text:
            print("✅ Results preview is displayed!")
            if 'Score:' in response.text:
                print("✅ Score is shown")
            if 'Question' in response.text:
                print("✅ Question details are visible")
            if 'Class Statistics' in response.text:
                print("✅ Class statistics are shown")
        else:
            print("❌ Results preview not found")
            
        # Check for the combined message
        if 'attempts remaining. Quiz feedback is limited' in response.text:
            print("✅ Combined message is displayed")
        else:
            print("❌ Combined message not found")
            
        print("\n" + "="*50 + "\n")
        
        # Test quiz 5 (Functions and Modules Quiz) - should NOT show results preview (no submission)
        print("Testing Quiz 5 (Functions and Modules Quiz)...")
        response2 = requests.get('http://localhost:5000/course/COMP101/quiz/5', cookies=cookies, timeout=10)
        
        print(f"Status Code: {response2.status_code}")
        print(f"Content Length: {len(response2.text)}")
        
        if 'Your Results Preview' in response2.text:
            print("❌ Results preview unexpectedly displayed for quiz 5")
        else:
            print("✅ Results preview correctly not shown for quiz 5")
            
        # Check for attempts remaining message only
        if 'attempts remaining' in response2.text and 'Quiz feedback is limited' not in response2.text:
            print("✅ Only attempts remaining message shown for quiz 5")
        else:
            print("❌ Message logic incorrect for quiz 5")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = test_quiz_info_page()
    sys.exit(0 if success else 1)