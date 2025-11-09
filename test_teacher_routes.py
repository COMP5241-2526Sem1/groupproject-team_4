#!/usr/bin/env python3
"""
Test script to verify teacher quiz routes are working correctly.
This script tests the new teacher quiz routes structure.
"""

import requests
import sys

def test_teacher_routes():
    """Test the teacher quiz routes"""
    base_url = "http://127.0.0.1:5000"
    
    # Test teacher quiz info route
    print("Testing teacher quiz info route...")
    try:
        response = requests.get(f"{base_url}/teacher/course/3/quiz/5")
        print(f"Teacher quiz info route status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Teacher quiz info route is accessible")
        elif response.status_code == 302:
            print("✅ Teacher quiz info route redirects (likely to login)")
        else:
            print(f"❌ Teacher quiz info route returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing teacher quiz info route: {e}")
    
    # Test teacher quiz start route
    print("\nTesting teacher quiz start route...")
    try:
        response = requests.get(f"{base_url}/teacher/course/3/quiz/5/start")
        print(f"Teacher quiz start route status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Teacher quiz start route is accessible")
        elif response.status_code == 302:
            print("✅ Teacher quiz start route redirects (likely to login)")
        else:
            print(f"❌ Teacher quiz start route returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing teacher quiz start route: {e}")
    
    # Test teacher quiz submit route
    print("\nTesting teacher quiz submit route...")
    try:
        response = requests.post(f"{base_url}/teacher/course/3/quiz/5/submit", data={})
        print(f"Teacher quiz submit route status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Teacher quiz submit route is accessible")
        elif response.status_code == 302:
            print("✅ Teacher quiz submit route redirects (likely to login)")
        elif response.status_code == 400:
            print("✅ Teacher quiz submit route validates data (expected)")
        else:
            print(f"❌ Teacher quiz submit route returned: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing teacher quiz submit route: {e}")
    
    print("\n" + "="*50)
    print("Teacher quiz routes test completed!")
    print("Routes tested:")
    print("- GET /teacher/course/<course_code>/quiz/<quiz_id>")
    print("- GET /teacher/course/<course_code>/quiz/<quiz_id>/start")
    print("- POST /teacher/course/<course_code>/quiz/<quiz_id>/submit")
    print("="*50)

if __name__ == "__main__":
    test_teacher_routes()