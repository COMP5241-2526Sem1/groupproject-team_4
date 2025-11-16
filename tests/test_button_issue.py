#!/usr/bin/env python3
"""
Test script to diagnose the Add Question button issue
"""

import requests
import time

def test_add_question_button():
    """Test if the Add Question button functionality works"""
    
    print("=== Testing Add Question Button Issue ===")
    
    # Test the quiz edit page
    try:
        # First, let's check if we can access the quiz edit page
        response = requests.get('http://127.0.0.1:5000/teacher/course/CS101/quiz/1/edit')
        
        if response.status_code == 200:
            print("✓ Quiz edit page accessible")
            
            # Check if the page contains the Add Question button
            if 'id="add-question-btn"' in response.text:
                print("✓ Add Question button found in HTML")
                
                # Check if JavaScript functions are present
                if 'function addQuestion()' in response.text:
                    print("✓ addQuestion function found in JavaScript")
                else:
                    print("✗ addQuestion function NOT found in JavaScript")
                
                # Check if DOMContentLoaded event listener is present
                if 'DOMContentLoaded' in response.text:
                    print("✓ DOMContentLoaded event listener found")
                else:
                    print("✗ DOMContentLoaded event listener NOT found")
                
                # Check if the button has proper event handling
                if 'addEventListener' in response.text and 'add-question-btn' in response.text:
                    print("✓ Event listener setup found")
                else:
                    print("✗ Event listener setup NOT found")
                
                # Check if onclick is present (backup method)
                if 'onclick' in response.text and 'addQuestion()' in response.text:
                    print("✓ Inline onclick handler found (backup)")
                else:
                    print("✗ Inline onclick handler NOT found")
                
                # Check for questions container
                if 'id="questions-container"' in response.text:
                    print("✓ Questions container found in HTML")
                else:
                    print("✗ Questions container NOT found in HTML")
                
            else:
                print("✗ Add Question button NOT found in HTML")
                print("  Available content preview:", response.text[:500] + "...")
                
            # Check for common JavaScript errors
            if 'SyntaxError' in response.text or 'ReferenceError' in response.text:
                print("⚠️  JavaScript errors detected in page")
            
            # Check for missing dependencies
            if 'jQuery' in response.text and 'jquery' not in response.text.lower():
                print("⚠️  jQuery referenced but may not be loaded")
                
            # Count total buttons on page
            button_count = response.text.count('<button')
            print(f"📊 Total buttons found on page: {button_count}")
                
        else:
            print(f"✗ Quiz edit page returned status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server - make sure Flask is running")
    except Exception as e:
        print(f"✗ Error testing page: {e}")
    
    print("\n=== Recommendations ===")
    print("1. Check browser console for JavaScript errors")
    print("2. Verify that the button is not hidden by CSS")
    print("3. Check if any JavaScript errors prevent event listeners from being attached")
    print("4. Try opening the page in an incognito/private browser window")
    print("5. Check browser developer tools Network tab for any failed requests")

if __name__ == '__main__':
    test_add_question_button()