#!/usr/bin/env python3
"""Test the pictures endpoint directly"""

import requests
import json

# Test the pictures endpoint directly
url = "http://127.0.0.1:5000/course/PHYS101/mini_games/9/pictures?last_update=0"
print(f"Testing URL: {url}")

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {list(data.keys())}")
        print(f"Pictures count: {len(data.get('pictures', []))}")
        print(f"Total count: {data.get('total_count', 0)}")
        
        if data.get('pictures'):
            print(f"First picture keys: {list(data['pictures'][0].keys())}")
            print(f"Sample picture data (first 100 chars): {str(data['pictures'][0])[:100]}...")
    else:
        print(f"Response text: {response.text}")
        
except Exception as e:
    print(f"Error: {e}")