#!/usr/bin/env python3
"""
Execute the clean SQL statements
"""

from app import app
from database import db
from sqlalchemy import text

def execute_clean_statements():
    """Execute the clean SQL statements"""
    
    with app.app_context():
        try:
            # Read the clean statements file
            with open('clean_statements.sql', 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("=== Executing Clean SQL Statements ===")
            
            # Split by semicolon and filter empty statements
            statements = [stmt.strip() for stmt in content.split(';') if stmt.strip()]
            
            print(f"Found {len(statements)} SQL statements to execute")
            
            # Execute each statement
            success_count = 0
            for i, statement in enumerate(statements):
                try:
                    # Extract table name for logging
                    if 'INSERT INTO' in statement.upper():
                        table_name = statement.upper().split('INSERT INTO')[1].split()[0]
                        print(f"Executing statement {i+1} into {table_name}")
                    else:
                        print(f"Executing statement {i+1}")
                    
                    db.session.execute(text(statement))
                    success_count += 1
                    
                except Exception as e:
                    print(f"Error in statement {i+1}: {e}")
                    print(f"Statement: {statement[:200]}...")
                    db.session.rollback()
                    return
            
            if success_count == len(statements):
                db.session.commit()
                print(f"✓ All {success_count} statements executed successfully")
                
                # Verify data was loaded
                tables = ['department', 'course', 'quiz', 'poll', 'short_answer', 'word_cloud', 'minigame', 'course_enrollment', 'question', 'choice', 'submission', 'attempt', 'question_response']
                
                for table in tables:
                    try:
                        result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.fetchone()[0]
                        print(f"{table}: {count}")
                    except Exception as e:
                        print(f"{table}: Error counting - {e}")
                        
            else:
                db.session.rollback()
                print(f"✗ Only {success_count}/{len(statements)} statements executed")
                
        except Exception as e:
            print(f"✗ Failed to load data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    execute_clean_statements()