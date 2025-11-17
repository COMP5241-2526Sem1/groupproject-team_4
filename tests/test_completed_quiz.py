import requests
import sys

def test_completed_quiz():
    """Test the quiz info page for a user who has completed all attempts"""
    
    # Test cookies for user 'a' who completed quiz 5
    cookies = {'session_id': 'user_a_session'}  # Using a different session
    
    try:
        # Test quiz 5 (Functions and Modules Quiz) - user 'a' has completed all attempts
        print("Testing Quiz 5 (Functions and Modules Quiz) for completed user...")
        response = requests.get('http://localhost:5000/course/COMP101/quiz/5', cookies=cookies, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        
        # Check if we can see results preview content
        if 'Your Results Preview' in response.text:
            print("✅ Results preview is displayed!")
            if 'Score:' in response.text or 'Grade:' in response.text:
                print("✅ Score/Grade is shown")
            if 'Question' in response.text:
                print("✅ Question details are visible")
            if 'Class Statistics' in response.text:
                print("✅ Class statistics are shown")
        else:
            print("❌ Results preview not found")
            
        # Check for completion message
        if 'completed this quiz and used all available attempts' in response.text:
            print("✅ Completion message is displayed")
        else:
            print("❌ Completion message not found")
            
        # Save response for debugging
        with open('completed_quiz_response.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("Response saved to completed_quiz_response.html for inspection")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = test_completed_quiz()
    sys.exit(0 if success else 1)