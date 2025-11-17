#!/usr/bin/env python3
"""
Test script for teacher course management features
This script tests the enhanced student management functionality
"""

import requests
import json
from urllib.parse import urljoin

class TeacherCourseManagementTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.csrf_token = None
        
    def login(self, username, password):
        """Login as teacher"""
        login_url = urljoin(self.base_url, '/login')
        
        # Get login page to extract CSRF token
        response = self.session.get(login_url)
        if 'csrf_token' in response.text:
            # Extract CSRF token from form
            import re
            csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', response.text)
            if csrf_match:
                self.csrf_token = csrf_match.group(1)
        
        # Submit login form
        login_data = {
            'username': username,
            'password': password,
            'csrf_token': self.csrf_token
        }
        
        response = self.session.post(login_url, data=login_data)
        return response.status_code == 200 and 'login' not in response.url
    
    def test_enrolled_students_list(self, course_id):
        """Test enrolled students list page"""
        url = urljoin(self.base_url, f'/teacher/course/{course_id}/enrolled_list')
        response = self.session.get(url)
        
        print(f"\n=== Testing Enrolled Students List (Course {course_id}) ===")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Check for enhanced features
            checks = [
                ('Modern CSS styling', 'student-container' in response.text),
                ('Checkbox on right side', 'student-checkbox' in response.text),
                ('Select All functionality', 'select-all' in response.text),
                ('Dynamic button states', 'updateRemoveButton' in response.text),
                ('Bulk remove functionality', 'bulk_remove_students' in response.text),
                ('Gradient buttons', 'background: linear-gradient' in response.text),
                ('Hover effects', 'transition: all 0.3s' in response.text)
            ]
            
            for feature, present in checks:
                status = "✓" if present else "✗"
                print(f"{status} {feature}")
            
            return True
        else:
            print(f"✗ Failed to load enrolled students list")
            return False
    
    def test_not_enrolled_students_list(self, course_id):
        """Test not enrolled students list page"""
        url = urljoin(self.base_url, f'/teacher/course/{course_id}/not_enrolled_list')
        response = self.session.get(url)
        
        print(f"\n=== Testing Not Enrolled Students List (Course {course_id}) ===")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # Check for enhanced features
            checks = [
                ('Modern CSS styling', 'student-container' in response.text),
                ('Checkbox on right side', 'student-checkbox' in response.text),
                ('Select All functionality', 'select-all' in response.text),
                ('Dynamic button states', 'updateAddButton' in response.text),
                ('Bulk add functionality', 'bulk_add_students' in response.text),
                ('Green gradient header', '#27ae60' in response.text),
                ('Capacity awareness', 'available_slots' in response.text)
            ]
            
            for feature, present in checks:
                status = "✓" if present else "✗"
                print(f"{status} {feature}")
            
            return True
        else:
            print(f"✗ Failed to load not enrolled students list")
            return False
    
    def test_import_students_page(self, course_id):
        """Test import students page"""
        url = urljoin(self.base_url, f'/teacher/course/{course_id}/import_students')
        response = self.session.get(url)
        
        print(f"\n=== Testing Import Students Page (Course {course_id}) ===")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            checks = [
                ('File upload form', 'csv_file' in response.text),
                ('Enhanced error handling', 'UTF-8' in response.text),
                ('CSV format validation', '.csv extension' in response.text)
            ]
            
            for feature, present in checks:
                status = "✓" if present else "✗"
                print(f"{status} {feature}")
            
            return True
        else:
            print(f"✗ Failed to load import students page")
            return False
    
    def run_comprehensive_test(self, username, password, course_id):
        """Run comprehensive test suite"""
        print("=" * 60)
        print("TEACHER COURSE MANAGEMENT FEATURES TEST")
        print("=" * 60)
        
        # Login
        print(f"\n=== Logging in as {username} ===")
        if self.login(username, password):
            print("✓ Login successful")
        else:
            print("✗ Login failed")
            return False
        
        # Test all features
        results = []
        results.append(self.test_enrolled_students_list(course_id))
        results.append(self.test_not_enrolled_students_list(course_id))
        results.append(self.test_import_students_page(course_id))
        
        # Summary
        print(f"\n=== TEST SUMMARY ===")
        passed = sum(results)
        total = len(results)
        print(f"Tests Passed: {passed}/{total}")
        
        if passed == total:
            print("🎉 All teacher course management features are working correctly!")
        else:
            print("⚠️  Some tests failed. Please check the implementation.")
        
        return passed == total

def main():
    """Main test function"""
    # Test configuration
    BASE_URL = "http://127.0.0.1:5000"
    TEACHER_USERNAME = "john_smith"  # From sample data
    TEACHER_PASSWORD = "password123"  # Default password from sample data
    TEST_COURSE_ID = 1  # Adjust as needed
    
    tester = TeacherCourseManagementTester(BASE_URL)
    
    try:
        success = tester.run_comprehensive_test(TEACHER_USERNAME, TEACHER_PASSWORD, TEST_COURSE_ID)
        return 0 if success else 1
    except requests.exceptions.ConnectionError:
        print(f"✗ Could not connect to {BASE_URL}")
        print("Please ensure the Flask application is running.")
        return 1
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())