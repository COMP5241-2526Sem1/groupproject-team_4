import requests
import re

# Create a session to maintain cookies
session = requests.Session()

# First, let's check if we can access the login page
try:
    login_response = session.get('http://localhost:5000/login', timeout=10)
    print('Login page status:', login_response.status_code)
    
    # Try to get the quiz page
    response = session.get('http://localhost:5000/course/PHYS101/quiz/6', timeout=10)
    
    print('Quiz page status:', response.status_code)
    print('Contains View Response button:', 'View Response' in response.text)
    print('Contains message section:', 'Notice:' in response.text)
    
    # Check if we're being redirected to login
    if 'login' in response.text.lower():
        print('Page redirects to login - authentication required')
    
    # Look for the View Response button specifically
    if 'View Response' in response.text:
        # Find the button HTML
        button_match = re.search(r'<button[^>]*>View Response</button>', response.text)
        if button_match:
            print('View Response button HTML:', button_match.group(0))
        
        # Check if it links to results page
        results_link = re.search(r'onclick="[^"]*results[^"]*"', response.text)
        if results_link:
            print('Results link found:', results_link.group(0))
    
    print('--- Page snippet ---')
    # Show a snippet around the button area or login redirect
    if 'login' in response.text.lower():
        login_pos = response.text.lower().find('login')
        start = max(0, login_pos - 100)
        end = min(len(response.text), login_pos + 100)
        print(response.text[start:end])
    elif 'View Response' in response.text:
        button_pos = response.text.find('View Response')
        start = max(0, button_pos - 200)
        end = min(len(response.text), button_pos + 200)
        print(response.text[start:end])
    else:
        # Show first 500 characters
        print(response.text[:500])

except Exception as e:
    print('Error:', str(e))