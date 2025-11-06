#!/usr/bin/env python3
"""
Simple test to verify database connection and basic quiz functionality
"""

from app import app
from database import db
from models.quiz import Quiz
from sqlalchemy import text

def test_simple():
    """Simple test without complex initialization"""
    
    with app.app_context():
        try:
            # Test basic database connection
            result = db.session.execute(text('SELECT 1')).fetchone()
            print(f"✓ Database connection works: {result}")
            
            # Test if quiz table exists
            try:
                quiz_count = db.session.query(Quiz).count()
                print(f"✓ Quiz table accessible, count: {quiz_count}")
                
                if quiz_count > 0:
                    quiz = db.session.query(Quiz).first()
                    print(f"✓ First quiz: ID={quiz.id}, Name='{quiz.name}'")
                else:
                    print("⚠ No quizzes found in database")
                    
            except Exception as e:
                print(f"⚠ Quiz table issue: {e}")
                
        except Exception as e:
            print(f"✗ Database connection failed: {e}")

if __name__ == "__main__":
    test_simple()