from app import app
from datetime import datetime

# Test template rendering with sample data
with app.app_context():
    # Mock poll data similar to what the route would pass
    test_polls = [
        {
            'id': 1,
            'name': 'Test Poll',
            'description': 'A test poll to verify date display',
            'used_attempts': 0,
            'max_attempts': 1,
            'can_attempt': True,
            'start_datetime': datetime(2024, 1, 15, 9, 0),  # Jan 15, 2024 9:00 AM
            'end_datetime': datetime(2024, 1, 15, 17, 0),   # Jan 15, 2024 5:00 PM
            'is_available': True
        },
        {
            'id': 2,
            'name': 'Another Test Poll',
            'description': 'Another test poll',
            'used_attempts': 1,
            'max_attempts': 1,
            'can_attempt': False,
            'start_datetime': datetime(2024, 1, 16, 10, 0), # Jan 16, 2024 10:00 AM
            'end_datetime': datetime(2024, 1, 16, 18, 0),  # Jan 16, 2024 6:00 PM
            'is_available': True
        }
    ]
    
    # Render the template with test data
    from flask import render_template
    html = render_template('poll_list.html', 
                          course={'code': 'COMP101', 'name': 'Test Course'},
                          polls=test_polls,
                          message=None)
    
    # Check if dates are in the HTML
    if 'Start Date' in html and 'End Date' in html:
        print("✓ Start and End dates are displayed in the template!")
        # Extract some sample content
        lines = html.split('\n')
        for i, line in enumerate(lines):
            if 'Start Date' in line or 'End Date' in line:
                print(f"Line {i}: {line.strip()}")
    else:
        print("✗ Start and End dates are NOT displayed in the template")
        print("Template preview:")
        print(html[:500])  # First 500 chars for debugging