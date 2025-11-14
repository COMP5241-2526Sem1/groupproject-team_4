#!/usr/bin/env python3
"""
Test SQL loading with better parsing
"""

from app import app
from database import db
from sqlalchemy import text

def test_sql_loading():
    """Test loading SQL with better parsing"""
    
    with app.app_context():
        try:
            # Read the SQL file
            with open('sample_data_refactored.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            print("=== Testing SQL Loading ===")
            
            # Split by semicolon and clean up
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            # Filter out comments and empty statements
            valid_statements = []
            for stmt in statements:
                # Skip comments and empty statements
                if stmt.startswith('--') or not stmt:
                    continue
                # Remove inline comments
                stmt_lines = []
                for line in stmt.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('--'):
                        stmt_lines.append(line)
                if stmt_lines:
                    valid_statements.append('\n'.join(stmt_lines))
            
            print(f"Found {len(valid_statements)} valid statements")
            
            # Execute each statement
            success_count = 0
            for i, statement in enumerate(valid_statements):
                try:
                    print(f"Executing statement {i+1}: {statement[:50]}...")
                    db.session.execute(text(statement))
                    success_count += 1
                except Exception as e:
                    print(f"Error in statement {i+1}: {e}")
                    print(f"Statement: {statement[:100]}...")
                    break
            
            if success_count == len(valid_statements):
                db.session.commit()
                print(f"✓ All {success_count} statements executed successfully")
            else:
                db.session.rollback()
                print(f"✗ Only {success_count}/{len(valid_statements)} statements executed")
            
            # Check results
            result = db.session.execute(text("SELECT COUNT(*) FROM department"))
            dept_count = result.fetchone()[0]
            print(f"Departments: {dept_count}")
            
            result = db.session.execute(text("SELECT COUNT(*) FROM course"))
            course_count = result.fetchone()[0]
            print(f"Courses: {course_count}")
            
            result = db.session.execute(text("SELECT COUNT(*) FROM quiz"))
            quiz_count = result.fetchone()[0]
            print(f"Quizzes: {quiz_count}")
            
        except Exception as e:
            print(f"✗ Failed to load data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    test_sql_loading()