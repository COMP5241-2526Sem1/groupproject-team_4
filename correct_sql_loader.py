#!/usr/bin/env python3
"""
Correct SQL loader that properly handles SQL structure
"""

from app import app
from database import db
from sqlalchemy import text

def load_sql_correct():
    """Load SQL with correct statement parsing"""
    
    with app.app_context():
        try:
            # Read the SQL file
            with open('sample_data_refactored.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            print("=== Loading SQL Data (Correct) ===")
            
            # Split by semicolon to get individual statements
            raw_statements = sql_content.split(';')
            
            # Process each statement
            statements = []
            for stmt in raw_statements:
                stmt = stmt.strip()
                if stmt:
                    # Remove comment lines but keep the actual SQL
                    clean_lines = []
                    for line in stmt.split('\n'):
                        line = line.strip()
                        # Skip comment-only lines, but keep lines with actual SQL
                        if line.startswith('--') and not any(keyword in line.upper() for keyword in ['INSERT', 'UPDATE', 'DELETE', 'SELECT']):
                            continue
                        clean_lines.append(line)
                    
                    if clean_lines:
                        clean_stmt = '\n'.join(clean_lines).strip()
                        if clean_stmt and not clean_stmt.startswith('--'):
                            statements.append(clean_stmt)
            
            print(f"Found {len(statements)} SQL statements")
            
            # Execute each statement
            success_count = 0
            for i, statement in enumerate(statements):
                try:
                    print(f"Executing statement {i+1}: {statement[:80]}...")
                    db.session.execute(text(statement))
                    success_count += 1
                except Exception as e:
                    print(f"Error in statement {i+1}: {e}")
                    print(f"Problem statement: {statement}")
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
                
                result = db.session.execute(text("SELECT COUNT(*) FROM question"))
                question_count = result.fetchone()[0]
                print(f"Questions: {question_count}")
                
                result = db.session.execute(text("SELECT COUNT(*) FROM submission"))
                submission_count = result.fetchone()[0]
                print(f"Submissions: {submission_count}")
                
            else:
                db.session.rollback()
                print(f"✗ Only {success_count}/{len(statements)} statements executed")
                
        except Exception as e:
            print(f"✗ Failed to load data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    load_sql_correct()