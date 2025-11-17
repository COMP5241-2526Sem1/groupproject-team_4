#!/usr/bin/env python3
"""Get full traceback from debugger"""

import requests
import re

def get_full_traceback():
    """Get the full traceback from the debugger"""
    session = requests.Session()
    
    # Login as teacher
    login_data = {
        "username": "t",
        "password": "comp5241",
        "role": "teacher"
    }
    
    response = session.post(
        "http://127.0.0.1:5000/login",
        json=login_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code != 200:
        print("Login failed!")
        return
    
    # Trigger the error
    dashboard_url = "http://127.0.0.1:5000/teacher/course/PHYS101/dashboard"
    response = session.get(dashboard_url)
    
    if response.status_code == 500:
        # Extract the debugger secret
        secret_match = re.search(r'SECRET = "([^"]*)"', response.text)
        if secret_match:
            secret = secret_match.group(1)
            print(f"Found debugger secret: {secret}")
            
            # Try to get the traceback
            traceback_url = f"http://127.0.0.1:5000/?__debugger__=yes&cmd=tb&frm=0&s={secret}"
            tb_response = session.get(traceback_url)
            print(f"Traceback response status: {tb_response.status_code}")
            print("Full traceback:")
            print(tb_response.text)

if __name__ == "__main__":
    get_full_traceback()