#!/usr/bin/env python3
"""Test the pictures endpoint with alice_johnson who is enrolled in PHYS101"""

import requests
import json

# First login as alice_johnson
login_url = "http://127.0.0.1:5000/login"
login_data = {
    "username": "alice_johnson",
    "password": "comp5241",
    "role": "student"
}

print("Logging in as alice_johnson...")
session = requests.Session()

response = session.post(login_url, json=login_data)
print(f"Login status: {response.status_code}")

if response.status_code == 200:
    print("Login successful!")
    
    # Test the pictures endpoint
    pictures_url = "http://127.0.0.1:5000/course/PHYS101/mini_games/9/pictures?last_update=0"
    print(f"Testing pictures endpoint: {pictures_url}")
    
    response = session.get(pictures_url)
    print(f"Pictures status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Pictures count: {len(data.get('pictures', []))}")
        print(f"Total count: {data.get('total_count', 0)}")
        
        if data.get('pictures'):
            print(f"First picture author: {data['pictures'][0].get('author_username', 'N/A')}")
            print(f"First picture description: {data['pictures'][0].get('description', 'N/A')}")
            print(f"First picture type: {data['pictures'][0].get('file_type', 'N/A')}")
            print(f"First picture data length: {len(str(data['pictures'][0].get('file_data', '')))}")
    else:
        print(f"Response text: {response.text}")
else:
    print(f"Login failed: {response.text}")