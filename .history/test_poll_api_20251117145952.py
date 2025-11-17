#!/usr/bin/env python3
import json
import requests

# Test the poll API directly
url = 'http://127.0.0.1:5000/api/ai/poll'

payload = {
    'topic': 'DNS services',
    'teaching_materials': '',
    'num_questions': 3
}

print(f"Testing poll API with payload: {payload}")

try:
    response = requests.post(
        url,
        json=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
except Exception as e:
    print(f"Error: {e}")
