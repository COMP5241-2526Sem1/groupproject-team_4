#!/usr/bin/env python3
"""
Manual SQL loader that extracts and executes individual INSERT statements
"""

from app import app
from database import db
from sqlalchemy import text
import re

def load_sql_manual():
    """Manually load SQL by extracting individual INSERT statements"""
    
    with app.app_context():
        try:
            # Read the SQL file
            with open('sample_data_refactored.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            print("=== Manual SQL Loading ===")
            
            # Extract INSERT statements using regex
            insert_pattern = r'INSERT INTO\s+(\w+)\s*\([^)]+\)\s*VALUES\s*\([^;]+\);'
            
            # Find all INSERT statements
            matches = re.findall(insert_pattern, sql_content, re.IGNORECASE | re.DOTALL)
            
            print(f"Found INSERT statements for tables: {matches}")
            
            # Extract full INSERT statements
            insert_statements = re.findall(r'INSERT INTO[\s\S]+?;', sql_content, re.IGNORECASE)
            
            print(f"Found {len(insert_statements)} INSERT statements")
            
            # Execute each INSERT statement
            success_count = 0
            for i, statement in enumerate(insert_statements):
                try:
                    # Clean up the statement
                    clean_statement = statement.strip().rstrip(';')
                    table_name = re.search(r'INSERT INTO\s+(\w+)', clean_statement, re.IGNORECASE).group(1)
                    print(f"Executing INSERT {i+1} into {table_name}")
                    
                    db.session.execute(text(clean_statement))
                    success_count += 1
                except Exception as e:
                    print(f"Error in INSERT {i+1}: {e}")
                    print(f"Statement: {clean_statement[:200]}...")
                    db.session.rollback()
                    return
            
            if success_count == len(insert_statements):
                db.session.commit()
                print(f"✓ All {success_count} INSERT statements executed successfully")
                
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
                print(f"✗ Only {success_count}/{len(insert_statements)} statements executed")
                
        except Exception as e:
            print(f"✗ Failed to load data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    load_sql_manual()