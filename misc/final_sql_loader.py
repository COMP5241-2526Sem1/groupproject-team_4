#!/usr/bin/env python3
"""
Final SQL loader with proper multi-line statement handling
"""

from app import app
from database import db
from sqlalchemy import text

def load_sql_final():
    """Load SQL with proper statement parsing"""
    
    with app.app_context():
        try:
            # Read the SQL file
            with open('sample_data_refactored.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            print("=== Loading SQL Data (Final) ===")
            
            # Split by semicolon, but preserve the full statements
            raw_statements = sql_content.split(';')
            
            # Clean up statements
            statements = []
            for stmt in raw_statements:
                stmt = stmt.strip()
                if stmt and not stmt.startswith('--') and not stmt.startswith('/*'):
                    # Remove any trailing comments
                    lines = []
                    for line in stmt.split('\n'):
                        clean_line = line.strip()
                        if clean_line and not clean_line.startswith('--'):
                            lines.append(clean_line)
                    
                    if lines:
                        full_statement = ' '.join(lines)
                        statements.append(full_statement)
            
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
    load_sql_final()