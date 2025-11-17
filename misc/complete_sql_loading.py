#!/usr/bin/env python3
"""
Complete SQL loading with all remaining data
"""

from app import app
from database import db
from sqlalchemy import text

def complete_sql_loading():
    """Complete loading all SQL data"""
    
    with app.app_context():
        try:
            print("=== Completing SQL Loading ===")
            
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
            
            # Load questions
            questions_stmt = '''INSERT INTO question (quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, type, content, points) VALUES 
            (%s, NULL, NULL, NULL, NULL, 'mcq', 'What is the correct way to declare a variable in Python?', 2),
            (%s, NULL, NULL, NULL, NULL, 'mcq', 'Which of the following is a Python data type?', 2),
            (%s, NULL, NULL, NULL, NULL, 'saq', 'Write a Python function to calculate the factorial of a number.', 6),
            (%s, NULL, NULL, NULL, NULL, 'mcq', 'What is the purpose of the "def" keyword in Python?', 3),
            (%s, NULL, NULL, NULL, NULL, 'mcq', 'How do you import a module in Python?', 2),
            (%s, NULL, NULL, NULL, NULL, 'mcq', 'What is the time complexity of binary search?', 5),
            (%s, NULL, NULL, NULL, NULL, 'mcq', 'Which data structure uses LIFO principle?', 3),
            (NULL, %s, NULL, NULL, NULL, 'mcq', 'How would you rate the course difficulty?', 0),
            (NULL, %s, NULL, NULL, NULL, 'mcq', 'What teaching method do you prefer?', 0),
            (NULL, %s, NULL, NULL, NULL, 'mcq', 'Do you prefer visual or textual learning materials?', 0),
            (NULL, NULL, %s, NULL, NULL, 'saq', 'Review the provided code and suggest three improvements.', 10),
            (NULL, NULL, %s, NULL, NULL, 'saq', 'Explain the time complexity of your suggested solution.', 10),
            (NULL, NULL, %s, NULL, NULL, 'saq', 'Describe your pendulum experiment procedure.', 15),
            (NULL, NULL, %s, NULL, NULL, 'saq', 'What were your key findings from the experiment?', 20)''' % (
                quiz_ids[0], quiz_ids[0], quiz_ids[0], quiz_ids[1], quiz_ids[1], quiz_ids[2], quiz_ids[2],
                poll_ids[0], poll_ids[0], poll_ids[1],
                short_answer_ids[0], short_answer_ids[0], short_answer_ids[1], short_answer_ids[1]
            )
            print("Loading questions...")
            db.session.execute(text(questions_stmt))
            
            # Get question IDs
            result = db.session.execute(text("SELECT id FROM question ORDER BY id"))
            question_ids = [row[0] for row in result.fetchall()]
            print(f"Question IDs: {question_ids}")
            
            # Load choices
            choices_stmt = '''INSERT INTO choice (question_id, content, is_correct) VALUES 
            (%s, 'var x = 5', false), (%s, 'x = 5', true), (%s, 'int x = 5', false), (%s, 'declare x = 5', false),
            (%s, 'Integer', true), (%s, 'String', true), (%s, 'Float', true), (%s, 'Character', false),
            (%s, 'To declare a variable', false), (%s, 'To define a function', true), (%s, 'To import a module', false), (%s, 'To create a class', false),
            (%s, 'include module_name', false), (%s, 'require module_name', false), (%s, 'import module_name', true), (%s, 'using module_name', false),
            (%s, 'O(n)', false), (%s, 'O(log n)', true), (%s, 'O(n log n)', false), (%s, 'O(n²)', false),
            (%s, 'Queue', false), (%s, 'Stack', true), (%s, 'Array', false), (%s, 'Tree', false),
            (%s, 'Very Easy', false), (%s, 'Easy', false), (%s, 'Moderate', false), (%s, 'Difficult', false),
            (%s, 'Lectures only', false), (%s, 'Hands-on practice', false), (%s, 'Group discussions', false), (%s, 'Mixed approach', false),
            (%s, 'Visual', false), (%s, 'Textual', false), (%s, 'Both equally', false), (%s, 'Depends on topic', false)''' % (
                question_ids[0], question_ids[0], question_ids[0], question_ids[0],
                question_ids[1], question_ids[1], question_ids[1], question_ids[1],
                question_ids[3], question_ids[3], question_ids[3], question_ids[3],
                question_ids[4], question_ids[4], question_ids[4], question_ids[4],
                question_ids[5], question_ids[5], question_ids[5], question_ids[5],
                question_ids[6], question_ids[6], question_ids[6], question_ids[6],
                question_ids[7], question_ids[7], question_ids[7], question_ids[7],
                question_ids[8], question_ids[8], question_ids[8], question_ids[8],
                question_ids[9], question_ids[9], question_ids[9], question_ids[9]
            )
            print("Loading choices...")
            db.session.execute(text(choices_stmt))
            
            # Get choice IDs
            result = db.session.execute(text("SELECT id FROM choice ORDER BY id"))
            choice_ids = [row[0] for row in result.fetchall()]
            print(f"Choice IDs: {choice_ids}")
            
            # Load submissions
            submissions_stmt = '''INSERT INTO submission (user_id, quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, submitted_at, grade) VALUES 
            (%s, %s, NULL, NULL, NULL, NULL, NOW() - INTERVAL '2 hours', 85.5),
            (%s, %s, NULL, NULL, NULL, NULL, NOW() - INTERVAL '1 hour', 92.0),
            (%s, %s, NULL, NULL, NULL, NULL, NOW() - INTERVAL '3 hours', 78.0),
            (%s, %s, NULL, NULL, NULL, NULL, NOW() - INTERVAL '30 minutes', 88.5),
            (%s, NULL, %s, NULL, NULL, NULL, NOW() - INTERVAL '1 day', NULL),
            (%s, NULL, %s, NULL, NULL, NULL, NOW() - INTERVAL '1 day', NULL),
            (%s, NULL, %s, NULL, NULL, NULL, NOW() - INTERVAL '2 days', NULL),
            (%s, NULL, NULL, %s, NULL, NULL, NOW() - INTERVAL '5 hours', 90.0),
            (%s, NULL, NULL, %s, NULL, NULL, NOW() - INTERVAL '1 day', 85.0)''' % (
                student_ids[0], quiz_ids[0], student_ids[0], quiz_ids[1], student_ids[1], quiz_ids[0], 
                student_ids[2], quiz_ids[2], student_ids[0], poll_ids[0], student_ids[1], poll_ids[0], 
                student_ids[2], poll_ids[1], student_ids[0], short_answer_ids[0], student_ids[3], short_answer_ids[1]
            )
            print("Loading submissions...")
            db.session.execute(text(submissions_stmt))
            
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
            
            # Load question responses
            responses_stmt = '''INSERT INTO question_response (submission_id, question_id, choice_id, text_answer, is_correct, points) VALUES 
            (%s, %s, %s, NULL, true, 2.0),
            (%s, %s, %s, NULL, true, 2.0),
            (%s, %s, NULL, 'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)', true, 6.0),
            (%s, %s, %s, NULL, true, 3.0),
            (%s, %s, %s, NULL, true, 2.0),
            (%s, %s, %s, NULL, true, 2.0),
            (%s, %s, %s, NULL, false, 1.0),
            (%s, %s, %s, NULL, true, 5.0),
            (%s, %s, %s, NULL, true, 3.0),
            (%s, %s, %s, NULL, false, 0.0),
            (%s, %s, %s, NULL, false, 0.0),
            (%s, %s, %s, NULL, false, 0.0),
            (%s, %s, %s, NULL, false, 0.0),
            (%s, %s, NULL, 'The code can be improved by: 1) Adding error handling, 2) Using more descriptive variable names, 3) Adding comments for clarity.', true, 10.0),
            (%s, %s, NULL, 'The time complexity is O(n log n) due to the sorting operation.', true, 10.0),
            (%s, %s, NULL, 'We measured the pendulum period for different lengths and masses.', true, 15.0),
            (%s, %s, NULL, 'The period increased with length but was independent of mass, confirming theoretical predictions.', true, 20.0)''' % (
                submission_ids[0], question_ids[0], choice_ids[1], submission_ids[0], question_ids[1], choice_ids[4], 
                submission_ids[0], question_ids[2], submission_ids[1], question_ids[3], choice_ids[9], 
                submission_ids[1], question_ids[4], choice_ids[14], submission_ids[2], question_ids[0], choice_ids[1], 
                submission_ids[2], question_ids[1], choice_ids[5], submission_ids[3], question_ids[5], choice_ids[17], 
                submission_ids[3], question_ids[6], choice_ids[21], submission_ids[4], question_ids[7], choice_ids[24], 
                submission_ids[5], question_ids[7], choice_ids[25], submission_ids[6], question_ids[8], choice_ids[28], 
                submission_ids[7], question_ids[10], submission_ids[7], question_ids[11], 
                submission_ids[8], question_ids[12], submission_ids[8], question_ids[13]
            )
            print("Loading question responses...")
            db.session.execute(text(responses_stmt))
            
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
    complete_sql_loading()