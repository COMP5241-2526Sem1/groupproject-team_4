#!/usr/bin/env python3
"""
Proper SQL loader that handles multi-line INSERT statements
"""

from app import app
from database import db
from sqlalchemy import text
import re

def load_sql_properly():
    """Load SQL with proper multi-line statement handling"""
    
    with app.app_context():
        try:
            # Read the SQL file
            with open('sample_data_refactored.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            print("=== Loading SQL Data ===")
            
            # Split by semicolon, but handle multi-line INSERT statements
            statements = []
            current_statement = []
            
            for line in sql_content.split('\n'):
                line = line.strip()
                
                # Skip comment lines
                if line.startswith('--') or not line:
                    continue
                    
                current_statement.append(line)
                
                # Check if this line ends with a semicolon (end of statement)
                if line.endswith(';'):
                    # Join the statement lines and clean up
                    full_statement = ' '.join(current_statement)
                    full_statement = full_statement.rstrip(';').strip()
                    if full_statement:
                        statements.append(full_statement)
                    current_statement = []
            
            # Handle any remaining statement
            if current_statement:
                full_statement = ' '.join(current_statement).strip()
                if full_statement:
                    statements.append(full_statement)
            
            print(f"Found {len(statements)} SQL statements")
            
            # Execute each statement
            success_count = 0
            for i, statement in enumerate(statements):
                try:
                    print(f"Executing statement {i+1}: {statement[:60]}...")
                    db.session.execute(text(statement))
                    success_count += 1
                except Exception as e:
                    print(f"Error in statement {i+1}: {e}")
                    print(f"Full statement: {statement}")
                    db.session.rollback()
                    return
            
            if success_count == len(statements):
                db.session.commit()
                print(f"✓ All {success_count} statements executed successfully")
                
                # Verify data was loaded
                result = db.session.execute(text("SELECT COUNT(*) FROM department"))
                dept_count = result.fetchone()[0]
                print(f"Departments: {dept_count}")
                
                result = db.session.execute(text("SELECT COUNT(*) FROM course"))
                course_count = result.fetchone()[0]
                print(f"Courses: {course_count}")
                
                result = db.session.execute(text("SELECT COUNT(*) FROM quiz"))
                quiz_count = result.fetchone()[0]
                print(f"Quizzes: {quiz_count}")
                
                result = db.session.execute(text("SELECT COUNT(*) FROM poll"))
                poll_count = result.fetchone()[0]
                print(f"Polls: {poll_count}")
                
                result = db.session.execute(text("SELECT COUNT(*) FROM short_answer"))
                short_answer_count = result.fetchone()[0]
                print(f"Short Answers: {short_answer_count}")
                
                result = db.session.execute(text("SELECT COUNT(*) FROM word_cloud"))
                word_cloud_count = result.fetchone()[0]
                print(f"Word Clouds: {word_cloud_count}")
                
                result = db.session.execute(text("SELECT COUNT(*) FROM minigame"))
                minigame_count = result.fetchone()[0]
                print(f"Minigames: {minigame_count}")
                
                result = db.session.execute(text("SELECT COUNT(*) FROM course_enrollment"))
                enrollment_count = result.fetchone()[0]
                print(f"Enrollments: {enrollment_count}")
                
            else:
                db.session.rollback()
                print(f"✗ Only {success_count}/{len(statements)} statements executed")
                
        except Exception as e:
            print(f"✗ Failed to load data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    load_sql_properly()