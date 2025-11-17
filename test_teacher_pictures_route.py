#!/usr/bin/env python3
"""Test if we can modify the pictures endpoint to allow teachers"""

import requests
import json

# First login as teacher
login_url = "http://127.0.0.1:5000/login"
login_data = {
    "username": "t",
    "password": "comp5241",
    "role": "teacher"
}

print("Logging in as teacher...")
session = requests.Session()

response = session.post(login_url, json=login_data)
print(f"Login status: {response.status_code}")

if response.status_code == 200:
    print("Login successful!")
    
    # Test if teacher can access pictures through teacher route
    teacher_pictures_url = "http://127.0.0.1:5000/teacher/course/PHYS101/mini_games/9/pictures?last_update=0"
    print(f"Testing teacher pictures endpoint: {teacher_pictures_url}")
    
    response = session.get(teacher_pictures_url)
    print(f"Teacher pictures status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Pictures count: {len(data.get('pictures', []))}")
        print(f"Total count: {data.get('total_count', 0)}")
    else:
        print(f"Response text: {response.text}")
        
    # Also test the regular endpoint
    regular_pictures_url = "http://127.0.0.1:5000/course/PHYS101/mini_games/9/pictures?last_update=0"
    print(f"Testing regular pictures endpoint: {regular_pictures_url}")
    
    response = session.get(regular_pictures_url)
    print(f"Regular pictures status: {response.status_code}")
    if response.status_code != 200:
        print(f"Response text: {response.text}")
else:
    print(f"Login failed: {response.text}")