import requests
import json

# Test student mini game detail view with alice_johnson
session = requests.Session()

# Try to login as alice_johnson
login_data = {
    'username': 'alice_johnson',
    'password': 'comp5241',
    'role': 'student'
}

print('Attempting student login with alice_johnson...')
login_response = session.post('http://127.0.0.1:5000/login', json=login_data)
print(f'Student login status: {login_response.status_code}')

if login_response.status_code == 200:
    print('Student login successful!')
    
    # Try to access student mini game detail view
    print('Accessing student mini game detail view...')
    response = session.get('http://127.0.0.1:5000/course/PHYS101/mini_games/9')
    print(f'Student mini game view status: {response.status_code}')
    
    if response.status_code == 200:
        content = response.text
        print(f'Content length: {len(content)}')
        
        # Check for key elements including drawings/pictures
        checks = {
            'Mini Game Details': 'Mini Game Details' in content,
            'Start Mini Game Button': 'Start Mini Game' in content,
            'Your Attempts': 'Your Attempts' in content,
            'Previous Attempts': 'Previous Attempts' in content,
            'Pictures Section': 'Pictures' in content,
            'Drawings': 'drawing' in content.lower() or 'draw' in content.lower(),
            'Images': 'img ' in content.lower() or 'image' in content.lower()
        }
        
        print('Element checks:')
        for element, found in checks.items():
            print(f'  {element}: {"✓" if found else "✗"}')
            
        # Check if it's a redirect (login page)
        if 'login' in response.url.lower() or 'Login' in content:
            print('⚠️  Redirected to login page - session may be invalid')
        elif 'Course List' in content:
            print('⚠️  Showing Course List instead of mini game details')
        else:
            print('✓ Page loaded successfully')
            # Save the full response for inspection
            with open('student_mini_game_response.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print('Full response saved to student_mini_game_response.html')
            # Show first 1000 chars for inspection
            print(f'First 1000 chars: {content[:1000]}')
    else:
        print(f'❌ Failed to access mini game view: {response.status_code}')
        if response.status_code == 302:
            print(f'Redirected to: {response.headers.get("Location", "unknown")}')
else:
    print(f'❌ Student login failed: {login_response.status_code}')
    if login_response.status_code == 401:
        print('Invalid credentials')
    print(f'Login response: {login_response.text[:200]}')