import unittest
from routes.auth import is_valid_email, is_valid_password
from flask import Flask
from flask.testing import FlaskClient

class TestAuthFunctions(unittest.TestCase):
    def test_is_valid_email(self):
        # Test valid email formats
        self.assertTrue(is_valid_email("user@example.com"))
        self.assertTrue(is_valid_email("user.name@example.com"))
        self.assertTrue(is_valid_email("user+name@example.com"))
        self.assertTrue(is_valid_email("user@sub.example.com"))
        
        # Test invalid email formats
        self.assertFalse(is_valid_email("user@example"))
        self.assertFalse(is_valid_email("user@.com"))
        self.assertFalse(is_valid_email("@example.com"))
        self.assertFalse(is_valid_email("user@example..com"))

    def test_is_valid_password(self):
        # Test valid passwords
        self.assertTrue(is_valid_password("Password123"))
        self.assertTrue(is_valid_password("pass123!@#"))
        self.assertTrue(is_valid_password("123abcDEF"))
        
        # Test invalid passwords
        self.assertFalse(is_valid_password("123456"))  # All digits
        self.assertFalse(is_valid_password("password"))  # No digits
        self.assertFalse(is_valid_password("123"))  # Too short

class TestAuthEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        # Mock database or other dependencies here

    def test_register_endpoint(self):
        # Test successful registration
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'Test123!',
            'role': 'student',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 201)
        
        # Test duplicate username
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'Test123!',
            'role': 'student',
            'email': 'testuser2@example.com'
        })
        self.assertEqual(response.status_code, 400)
        
        # Test invalid email
        response = self.client.post('/register', json={
            'username': 'testuser2',
            'password': 'Test123!',
            'role': 'student',
            'email': 'invalid-email'
        })
        self.assertEqual(response.status_code, 400)
        
        # Test invalid password
        response = self.client.post('/register', json={
            'username': 'testuser3',
            'password': '123456',
            'role': 'student',
            'email': 'testuser3@example.com'
        })
        self.assertEqual(response.status_code, 400)

    def test_login_endpoint(self):
        # Test successful login
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'Test123!'
        })
        self.assertEqual(response.status_code, 200)
        
        # Test invalid credentials
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()