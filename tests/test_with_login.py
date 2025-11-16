# Test the quiz info page with proper login
import requests
import json

# Create a session to maintain cookies
session = requests.Session()

# First, get the login page
login_response = session.get('http://localhost:5000/login')
print(f'Login page status: {login_response.status_code}')

# Try to login with JSON data (as the JavaScript does)
login_data = {
    'username': 'carol_davis',
    'password': 'comp5241',  # This is the password from the SQL data
    'role': 'student'
}

login_submit = session.post('http://localhost:5000/login', 
                            headers={'Content-Type': 'application/json'},
                            data=json.dumps(login_data))
print(f'Login submit status: {login_submit.status_code}')

# Check if login was successful by looking at the response
login_response_data = json.loads(login_submit.text)
if login_submit.status_code == 200 and login_response_data.get('msg') == 'login success!':
    print("Login successful")
    
    # Now try to access the quiz info page
    quiz_response = session.get('http://localhost:5000/course/COMP201/quiz/6')
    print(f'Quiz page status: {quiz_response.status_code}')
    
    if quiz_response.status_code == 200:
        content = quiz_response.text
        
        # Check for View Response button
        has_view_response = 'View Response' in content
        print(f'Contains View Response button: {has_view_response}')
        
        # Check for the message section (should be removed)
        has_message = 'You have already attempted this quiz' in content
        print(f'Contains message section: {has_message}')
        
        # Check for results link
        has_results_link = '/course/COMP201/quiz/6/results' in content
        print(f'Contains results link: {has_results_link}')
        
        # Show a snippet around the button area
        if has_view_response:
            # Find the button area
            import re
            button_match = re.search(r'<div[^>]*style="[^"]*margin-top: 20px[^"]*"[^>]*>.*?</div>', content, re.DOTALL)
            if button_match:
                print(f'Button area snippet: {button_match.group(0)}')
            else:
                print('Could not find button area')
        else:
            # Show a snippet of the page content
            snippet_start = max(0, len(content) - 500)
            print(f'Page snippet (last 500 chars): {content[snippet_start:]}')
    else:
        print('Failed to access quiz page')
        print(f'Response content: {quiz_response.text[:500]}')
else:
    print('Login failed')
    print(f'Login response: {login_submit.text[:500]}')