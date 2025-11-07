#!/usr/bin/env python3
"""
Create a test teacher account for testing the Add Question functionality
"""

import os
import sys

def create_test_teacher():
    """Create a test teacher account"""
    
    print("🎓 Creating test teacher account...")
    
    try:
        # Import required modules
        from app import app, db
        from models.user import User
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            # Check if teacher already exists
            existing_teacher = User.query.filter_by(username="test_teacher").first()
            if existing_teacher:
                print("ℹ️  Test teacher account already exists")
                print("   Username: test_teacher")
                print("   Password: test123")
                print("   Role: teacher")
                return True
            
            # Create new teacher account
            teacher = User(
                username="test_teacher",
                email="teacher@test.com",
                role="teacher"
            )
            teacher.password_hash = generate_password_hash("test123")
            
            db.session.add(teacher)
            db.session.commit()
            
            print("✅ Test teacher account created successfully!")
            print("   Username: test_teacher")
            print("   Password: test123")
            print("   Email: teacher@test.com")
            print("   Role: teacher")
            print("   Status: Approved")
            
            return True
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running this from the project root directory")
        return False
    except Exception as e:
        print(f"❌ Error creating teacher account: {e}")
        return False

def create_test_course():
    """Create a test course for the teacher"""
    
    print("\n📚 Creating test course...")
    
    try:
        from app import app, db
        from models.course import Course
        from models.user import User
        
        with app.app_context():
            # Find the test teacher
            teacher = User.query.filter_by(username="test_teacher").first()
            if not teacher:
                print("❌ Test teacher not found, please create teacher first")
                return False
            
            # Check if course already exists
            existing_course = Course.query.filter_by(code="CS101").first()
            if existing_course:
                print("ℹ️  Test course CS101 already exists")
                return True
            
            # Create new course
            from datetime import time
            course = Course(
                code="CS101",
                name="Introduction to Computer Science",
                teacher_id=teacher.id,
                description="Test course for Add Question functionality",
                capacity=50,
                day_of_week="Mon",
                start_time=time(9, 0),
                end_time=time(11, 0),
                course_number="101"
            )
            
            db.session.add(course)
            db.session.commit()
            
            print("✅ Test course created successfully!")
            print("   Course Code: CS101")
            print("   Course Name: Introduction to Computer Science")
            print("   Teacher: test_teacher")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating course: {e}")
        return False

def create_test_quiz():
    """Create a test quiz for the course"""
    
    print("\n📝 Creating test quiz...")
    
    try:
        from app import app, db
        from models.course import Course
        from models.quiz import Quiz
        from models.user import User
        
        with app.app_context():
            # Find the test teacher and course
            teacher = User.query.filter_by(username="test_teacher").first()
            course = Course.query.filter_by(code="CS101").first()
            
            if not teacher:
                print("❌ Test teacher not found, please create teacher first")
                return False
                
            if not course:
                print("❌ Test course not found, please create course first")
                return False
            
            # Check if quiz already exists
            existing_quiz = Quiz.query.filter_by(course_code=course.code, name="Test Quiz").first()
            if existing_quiz:
                print("ℹ️  Test quiz already exists")
                return True
            
            # Create new quiz
            quiz = Quiz(
                name="Test Quiz",
                description="Test quiz for Add Question functionality",
                course_code=course.code,
                created_by=teacher.id,
                duration=60,
                point=100
            )
            
            db.session.add(quiz)
            db.session.commit()
            
            print("✅ Test quiz created successfully!")
            print("   Quiz Title: Test Quiz")
            print("   Course: CS101")
            print("   Time Limit: 60 minutes")
            print("   Total Marks: 100")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creating quiz: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Setting up test environment for Add Question functionality...")
    print("=" * 60)
    
    # Create test teacher
    if create_test_teacher():
        # Create test course
        if create_test_course():
            # Create test quiz
            if create_test_quiz():
                print("\n" + "=" * 60)
                print("🎉 Test environment setup complete!")
                print("\n📋 Test Credentials:")
                print("   Username: test_teacher")
                print("   Password: test123")
                print("   Course: CS101")
                print("   Quiz: Test Quiz (ID: 1)")
                print("\n🔗 Test URL:")
                print("   http://127.0.0.1:5000/teacher/course/CS101/quiz/1/edit")
                print("\n✨ Instructions:")
                print("1. Start the Flask server: python app.py")
                print("2. Go to the login page: http://127.0.0.1:5000/login")
                print("3. Log in with test_teacher / test123")
                print("4. Navigate to the quiz edit page")
                print("5. Test the Add Question button!")
            else:
                print("\n❌ Failed to create test quiz")
        else:
            print("\n❌ Failed to create test course")
    else:
        print("\n❌ Failed to create test teacher")