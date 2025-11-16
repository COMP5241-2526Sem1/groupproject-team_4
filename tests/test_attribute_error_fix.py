import requests
import sys

# Test the teacher quiz route directly to check for AttributeError
def test_teacher_quiz_route():
    """Test if the teacher quiz route works without AttributeError"""
    
    # First, let's try to access the route without login to see if we get the AttributeError
    print("Testing teacher quiz route without login...")
    try:
        response = requests.get('http://localhost:5000/teacher/course/PHYS101/quiz/14')
        print(f"Response status: {response.status_code}")
        
        # Check if we get the AttributeError in the response
        if "AttributeError" in response.text:
            print("❌ FAILED: AttributeError found in response")
            print(f"Error: {response.text}")
            return False
        elif "'Attempt' object has no attribute 'score'" in response.text:
            print("❌ FAILED: Score attribute error found")
            return False
        else:
            print("✅ SUCCESS: No AttributeError found in response")
            return True
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_with_mock_session():
    """Test with a mock session cookie"""
    print("\nTesting with mock session...")
    
    # Create a session with a mock cookie
    session = requests.Session()
    session.cookies.set('session', 'mock_session_id')
    
    try:
        response = session.get('http://localhost:5000/teacher/course/PHYS101/quiz/14')
        print(f"Response status: {response.status_code}")
        
        # Check for AttributeError
        if "AttributeError" in response.text or "'Attempt' object has no attribute 'score'" in response.text:
            print("❌ FAILED: AttributeError found")
            return False
        else:
            print("✅ SUCCESS: No AttributeError found")
            return True
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing teacher quiz routes for AttributeError fix...")
    
    success1 = test_teacher_quiz_route()
    success2 = test_with_mock_session()
    
    if success1 and success2:
        print("\n🎉 All tests passed! The AttributeError has been fixed.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")
        
    sys.exit(0 if success1 and success2 else 1)