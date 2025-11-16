#!/usr/bin/env python3
"""
Clean SQL loader that properly separates comments from SQL statements
"""

from app import app
from database import db
from sqlalchemy import text

def load_sql_clean():
    """Load SQL with proper comment separation"""
    
    with app.app_context():
        try:
            # Read the SQL file
            with open('sample_data_refactored.sql', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            print("=== Clean SQL Loading ===")
            
            # Build complete statements, ignoring comments
            statements = []
            current_statement = ""
            
            for line in lines:
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Skip comment lines (but not lines that contain SQL with comments)
                if line.startswith('--') and not any(keyword in line.upper() for keyword in ['INSERT', 'UPDATE', 'DELETE', 'SELECT']):
                    continue
                
                # Add line to current statement
                current_statement += line + " "
                
                # If line ends with semicolon, we have a complete statement
                if line.endswith(';'):
                    # Clean up the statement
                    clean_stmt = current_statement.strip()
                    
                    # Remove inline comments but keep the SQL
                    clean_lines = []
                    for stmt_line in clean_stmt.split('\n'):
                        stmt_line = stmt_line.strip()
                        if stmt_line.startswith('--') and not any(keyword in stmt_line.upper() for keyword in ['INSERT', 'UPDATE', 'DELETE', 'SELECT']):
                            continue
                        clean_lines.append(stmt_line)
                    
                    final_stmt = '\n'.join(clean_lines).strip()
                    if final_stmt:
                        statements.append(final_stmt)
                    current_statement = ""
            
            print(f"Built {len(statements)} SQL statements")
            
            # Execute each statement
            success_count = 0
            for i, statement in enumerate(statements):
                try:
                    # Remove trailing semicolon for execution
                    clean_statement = statement.rstrip(';').strip()
                    
                    # Extract table name for logging
                    if 'INSERT INTO' in clean_statement.upper():
                        table_name = clean_statement.upper().split('INSERT INTO')[1].split()[0]
                        print(f"Executing statement {i+1} into {table_name}")
                    else:
                        print(f"Executing statement {i+1}")
                    
                    db.session.execute(text(clean_statement))
                    success_count += 1
                    
                except Exception as e:
                    print(f"Error in statement {i+1}: {e}")
                    print(f"Statement: {clean_statement[:200]}...")
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
    load_sql_clean()