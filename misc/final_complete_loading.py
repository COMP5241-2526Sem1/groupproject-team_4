#!/usr/bin/env python3
"""
Final complete SQL loading with fixed format strings
"""

from app import app
from database import db
from sqlalchemy import text

def final_complete_loading():
    """Final complete loading all SQL data"""
    
    with app.app_context():
        try:
            print("=== Final Complete SQL Loading ===")
            
            # Get current IDs for reference
            result = db.session.execute(text("SELECT id FROM quiz ORDER BY id"))
            quiz_ids = [row[0] for row in result.fetchall()]
            print(f"Quiz IDs: {quiz_ids}")
            
            result = db.session.execute(text("SELECT id FROM poll ORDER BY id"))
            poll_ids = [row[0] for row in result.fetchall()]
            print(f"Poll IDs: {poll_ids}")
            
            result = db.session.execute(text("SELECT id FROM short_answer ORDER BY id"))
            short_answer_ids = [row[0] for row in result.fetchall()]
            print(f"Short Answer IDs: {short_answer_ids}")
            
            result = db.session.execute(text("SELECT id FROM word_cloud ORDER BY id"))
            word_cloud_ids = [row[0] for row in result.fetchall()]
            print(f"Word Cloud IDs: {word_cloud_ids}")
            
            result = db.session.execute(text("SELECT id FROM minigame ORDER BY id"))
            minigame_ids = [row[0] for row in result.fetchall()]
            print(f"Minigame IDs: {minigame_ids}")
            
            result = db.session.execute(text("SELECT id FROM \"user\" WHERE role = 'student' ORDER BY id"))
            student_ids = [row[0] for row in result.fetchall()]
            print(f"Student IDs: {student_ids}")
            
            # Get question IDs
            result = db.session.execute(text("SELECT id FROM question ORDER BY id"))
            question_ids = [row[0] for row in result.fetchall()]
            print(f"Question IDs: {question_ids}")
            
            # Get choice IDs
            result = db.session.execute(text("SELECT id FROM choice ORDER BY id"))
            choice_ids = [row[0] for row in result.fetchall()]
            print(f"Choice IDs: {choice_ids}")
            
            # Get submission IDs
            result = db.session.execute(text("SELECT id FROM submission ORDER BY id"))
            submission_ids = [row[0] for row in result.fetchall()]
            print(f"Submission IDs: {submission_ids}")
            
            # Load attempts
            attempts_stmt = '''INSERT INTO attempt (quiz_id, user_id, attempt_count, created_at) VALUES 
            (%s, %s, 1, NOW() - INTERVAL '3 hours'),
            (%s, %s, 2, NOW() - INTERVAL '2 hours'),
            (%s, %s, 1, NOW() - INTERVAL '4 hours'),
            (%s, %s, 1, NOW() - INTERVAL '2 hours'),
            (%s, %s, 1, NOW() - INTERVAL '1 hour')''' % (
                quiz_ids[0], student_ids[0], quiz_ids[0], student_ids[0], quiz_ids[0], student_ids[1], 
                quiz_ids[1], student_ids[0], quiz_ids[2], student_ids[2]
            )
            print("Loading attempts...")
            db.session.execute(text(attempts_stmt))
            
            # Load question responses - fix the format string
            responses_data = [
                (submission_ids[0], question_ids[0], choice_ids[1], None, True, 2.0),
                (submission_ids[0], question_ids[1], choice_ids[4], None, True, 2.0),
                (submission_ids[0], question_ids[2], None, 'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)', True, 6.0),
                (submission_ids[1], question_ids[3], choice_ids[9], None, True, 3.0),
                (submission_ids[1], question_ids[4], choice_ids[14], None, True, 2.0),
                (submission_ids[2], question_ids[0], choice_ids[1], None, True, 2.0),
                (submission_ids[2], question_ids[1], choice_ids[5], None, False, 1.0),
                (submission_ids[3], question_ids[5], choice_ids[17], None, True, 5.0),
                (submission_ids[3], question_ids[6], choice_ids[21], None, True, 3.0),
                (submission_ids[4], question_ids[7], choice_ids[24], None, False, 0.0),
                (submission_ids[5], question_ids[7], choice_ids[25], None, False, 0.0),
                (submission_ids[6], question_ids[8], choice_ids[28], None, False, 0.0),
                (submission_ids[6], question_ids[9], choice_ids[32], None, False, 0.0),
                (submission_ids[7], question_ids[10], None, 'The code can be improved by: 1) Adding error handling, 2) Using more descriptive variable names, 3) Adding comments for clarity.', True, 10.0),
                (submission_ids[7], question_ids[11], None, 'The time complexity is O(n log n) due to the sorting operation.', True, 10.0),
                (submission_ids[8], question_ids[12], None, 'We measured the pendulum period for different lengths and masses.', True, 15.0),
                (submission_ids[8], question_ids[13], None, 'The period increased with length but was independent of mass, confirming theoretical predictions.', True, 20.0)
            ]
            
            print("Loading question responses...")
            for i, (sub_id, q_id, choice_id, text_answer, is_correct, points) in enumerate(responses_data):
                if choice_id:
                    stmt = "INSERT INTO question_response (submission_id, question_id, choice_id, text_answer, is_correct, points) VALUES (%s, %s, %s, %s, %s, %s)"
                    db.session.execute(text(stmt), (sub_id, q_id, choice_id, text_answer, is_correct, points))
                else:
                    stmt = "INSERT INTO question_response (submission_id, question_id, text_answer, is_correct, points) VALUES (%s, %s, %s, %s, %s)"
                    db.session.execute(text(stmt), (sub_id, q_id, text_answer, is_correct, points))
            
            # Commit all changes
            db.session.commit()
            print("✓ All data loaded successfully!")
            
            # Final verification
            tables = ['department', 'course', 'quiz', 'poll', 'short_answer', 'word_cloud', 'minigame', 'course_enrollment', 'question', 'choice', 'submission', 'attempt', 'question_response']
            
            for table in tables:
                try:
                    result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"{table}: {count}")
                except Exception as e:
                    print(f"{table}: Error counting - {e}")
                    
        except Exception as e:
            print(f"✗ Failed to complete loading: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    final_complete_loading()