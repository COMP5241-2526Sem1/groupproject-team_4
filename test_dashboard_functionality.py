#!/usr/bin/env python3
"""
Test script to verify the student dashboard functionality
"""

import requests
import sys

def test_dashboard_functionality():
    """Test the new dashboard functionality"""
    print("🧪 Testing Student Dashboard Functionality...")
    
    # Login as student
    session = requests.Session()
    login_data = {
        'username': 'alice_johnson',
        'password': 'securepass123'
    }
    
    print("Logging in as student...")
    response = session.post('http://127.0.0.1:5000/login', data=login_data)
    
    if response.status_code != 200:
        print("❌ Login failed")
        return False
    
    print("✅ Login successful")
    
    # Test dashboard route
    print("Testing dashboard route...")
    dashboard_response = session.get('http://127.0.0.1:5000/course/COMP101/dashboard')
    
    if dashboard_response.status_code != 200:
        print(f"❌ Dashboard route failed with status {dashboard_response.status_code}")
        return False
    
    dashboard_html = dashboard_response.text
    print("✅ Dashboard route accessible")
    
    # Check for required elements
    required_elements = [
        'Activity Progress',
        'Class Participation Leaderboard', 
        'Quick Actions',
        'ring-chart',
        'leaderboard-table',
        'Take Quiz',
        'Play Games',
        'Join Poll',
        'View Grades'
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in dashboard_html:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing elements: {missing_elements}")
        return False
    
    print("✅ All required dashboard elements found")
    
    # Check for ring chart with 3/5 indicator
    if '3' in dashboard_html and '/ 5' in dashboard_html:
        print("✅ Ring chart shows 3/5 completed activities")
    else:
        print("❌ Ring chart doesn't show correct 3/5 indicator")
        return False
    
    # Check for leaderboard table structure
    if '<table>' in dashboard_html and '<thead>' in dashboard_html:
        print("✅ Leaderboard table structure found")
    else:
        print("❌ Leaderboard table structure missing")
        return False
    
    print("🎉 Dashboard functionality test passed!")
    return True

if __name__ == "__main__":
    success = test_dashboard_functionality()
    sys.exit(0 if success else 1)