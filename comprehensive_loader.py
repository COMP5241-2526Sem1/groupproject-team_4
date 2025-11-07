#!/usr/bin/env python3
"""
Comprehensive SQL loader that loads all data in correct order
"""

from app import app
from database import db
from sqlalchemy import text

def comprehensive_load():
    """Comprehensive loading of all SQL data in correct order"""
    
    with app.app_context():
        try:
            print("=== Comprehensive SQL Loading ===")
            
            # Check existing data first
            print("Checking existing data...")
            tables = ['department', 'course', 'quiz', 'poll', 'short_answer', 'word_cloud', 'minigame', 'course_enrollment', 'question', 'choice', 'submission', 'attempt', 'question_response', 'user']
            
            existing_counts = {}
            for table in tables:
                try:
                    result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    existing_counts[table] = count
                    print(f"{table}: {count} existing records")
                except:
                    existing_counts[table] = 0
                    print(f"{table}: 0 existing records")
            
            # Load departments (skip if they exist)
            if existing_counts['department'] == 0:
                print("Loading departments...")
                dept_stmt = "INSERT INTO department (name, full_name) VALUES ('COMP', 'Department of Computer Science'), ('MATH', 'Department of Mathematics'), ('PHYS', 'Department of Physics'), ('CHEM', 'Department of Chemistry'), ('ENG', 'Department of English')"
                db.session.execute(text(dept_stmt))
            else:
                print("Departments already exist, skipping...")
            
            # Load users (skip if they exist)
            if existing_counts['user'] == 0:
                print("Loading users...")
                user_stmt = '''INSERT INTO "user" (username, password_hash, role, email, department_code, created_at) VALUES 
                ('john_smith', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'teacher', 'john.smith@university.edu', 'COMP', NOW()), 
                ('maria_garcia', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'teacher', 'maria.garcia@university.edu', 'MATH', NOW()), 
                ('david_chen', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'teacher', 'david.chen@university.edu', 'PHYS', NOW()), 
                ('alice_johnson', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'alice.j@student.edu', 'COMP', NOW()), 
                ('bob_williams', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'bob.w@student.edu', 'COMP', NOW()), 
                ('carol_davis', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'carol.d@student.edu', 'MATH', NOW()), 
                ('daniel_miller', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'daniel.m@student.edu', 'PHYS', NOW()), 
                ('emma_wilson', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'emma.w@student.edu', 'CHEM', NOW()), 
                ('frank_thomas', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'frank.t@student.edu', 'ENG', NOW())'''
                db.session.execute(text(user_stmt))
            else:
                print("Users already exist, skipping...")
            
            # Get user IDs
            result = db.session.execute(text("SELECT id, username FROM \"user\" ORDER BY id"))
            users = result.fetchall()
            teacher_ids = [user[0] for user in users if user[1].endswith('_smith') or user[1].endswith('_garcia') or user[1].endswith('_chen')]
            student_ids = [user[0] for user in users if user[1].endswith('_johnson') or user[1].endswith('_williams') or user[1].endswith('_davis') or user[1].endswith('_miller') or user[1].endswith('_wilson') or user[1].endswith('_thomas')]
            
            print(f"Teacher IDs: {teacher_ids}")
            print(f"Student IDs: {student_ids}")
            
            # Load courses (skip if they exist)
            if existing_counts['course'] == 0:
                print("Loading courses...")
                course_stmt = '''INSERT INTO course (code, name, description, department_code, teacher_id, created_at, credit, capacity, day_of_week, start_time, end_time, course_number) VALUES 
                ('COMP101', 'Introduction to Programming', 'Learn Python programming fundamentals', 'COMP', %s, NOW(), 3, 30, 'Mon', '09:00:00', '11:00:00', '101'), 
                ('COMP201', 'Data Structures', 'Advanced data structures and algorithms', 'COMP', %s, NOW(), 3, 25, 'Wed', '14:00:00', '16:00:00', '201'), 
                ('MATH101', 'Calculus I', 'Differential calculus', 'MATH', %s, NOW(), 4, 35, 'Tue', '10:00:00', '12:00:00', '101'), 
                ('PHYS101', 'Physics I', 'Mechanics and thermodynamics', 'PHYS', %s, NOW(), 4, 30, 'Thu', '13:00:00', '15:00:00', '101'), 
                ('ENG101', 'English Composition', 'Academic writing and composition', 'ENG', %s, NOW(), 3, 25, 'Fri', '11:00:00', '13:00:00', '101')''' % (
                    teacher_ids[0], teacher_ids[0], teacher_ids[1], teacher_ids[2], teacher_ids[2]
                )
                db.session.execute(text(course_stmt))
            else:
                print("Courses already exist, skipping...")
            
            # Load course enrollments (skip if they exist)
            if existing_counts['course_enrollment'] == 0:
                print("Loading course enrollments...")
                enrollment_stmt = '''INSERT INTO course_enrollment (course_code, student_id, enrolled_at) VALUES 
                ('COMP101', %s, NOW() - INTERVAL '10 days'), 
                ('COMP101', %s, NOW() - INTERVAL '9 days'), 
                ('COMP201', %s, NOW() - INTERVAL '8 days'), 
                ('MATH101', %s, NOW() - INTERVAL '7 days'), 
                ('PHYS101', %s, NOW() - INTERVAL '6 days'), 
                ('ENG101', %s, NOW() - INTERVAL '5 days')''' % (
                    student_ids[0], student_ids[1], student_ids[0], student_ids[2], student_ids[3], student_ids[5]
                )
                db.session.execute(text(enrollment_stmt))
            else:
                print("Course enrollments already exist, skipping...")
            
            # Load quizzes (skip if they exist)
            if existing_counts['quiz'] == 0:
                print("Loading quizzes...")
                quiz_stmt = '''INSERT INTO quiz (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) VALUES 
                ('COMP101', 'Python Basics Quiz', 'Test your understanding of Python fundamentals', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '7 days', 30, 3, 100, 20, true, false, true, true), 
                ('COMP101', 'Functions and Modules Quiz', 'Assessment on functions and module usage', %s, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', 25, 2, 100, 15, true, true, true, false), 
                ('COMP201', 'Data Structures Quiz', 'Quiz on arrays, lists, and trees', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '10 days', 45, 5, 100, 25, false, true, true, true)''' % (
                    teacher_ids[0], teacher_ids[0], teacher_ids[0]
                )
                db.session.execute(text(quiz_stmt))
            else:
                print("Quizzes already exist, skipping...")
            
            # Get quiz IDs
            result = db.session.execute(text("SELECT id FROM quiz ORDER BY id"))
            quiz_ids = [row[0] for row in result.fetchall()]
            
            # Load polls (skip if they exist)
            if existing_counts['poll'] == 0:
                print("Loading polls...")
                poll_stmt = '''INSERT INTO poll (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) VALUES 
                ('COMP101', 'Course Feedback Poll', 'Help us improve the course', %s, NOW(), NOW() - INTERVAL '3 days', NOW() + INTERVAL '4 days', 15, 1, 0, 0, true, true, true, true), 
                ('MATH101', 'Learning Style Poll', 'What helps you learn best?', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '6 days', 10, 1, 0, 0, true, true, true, true)''' % (
                    teacher_ids[0], teacher_ids[1]
                )
                db.session.execute(text(poll_stmt))
            else:
                print("Polls already exist, skipping...")
            
            # Get poll IDs
            result = db.session.execute(text("SELECT id FROM poll ORDER BY id"))
            poll_ids = [row[0] for row in result.fetchall()]
            
            # Load short answers (skip if they exist)
            if existing_counts['short_answer'] == 0:
                print("Loading short answers...")
                short_answer_stmt = '''INSERT INTO short_answer (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES 
                ('COMP101', 'Code Review Assignment', 'Review and improve given code', %s, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '8 days', 60, 1, 100, 30), 
                ('PHYS101', 'Physics Lab Report', 'Write a lab report on pendulum experiment', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '12 days', 120, 1, 100, 35)''' % (
                    teacher_ids[0], teacher_ids[2]
                )
                db.session.execute(text(short_answer_stmt))
            else:
                print("Short answers already exist, skipping...")
            
            # Get short answer IDs
            result = db.session.execute(text("SELECT id FROM short_answer ORDER BY id"))
            short_answer_ids = [row[0] for row in result.fetchall()]
            
            # Load word clouds (skip if they exist)
            if existing_counts['word_cloud'] == 0:
                print("Loading word clouds...")
                word_cloud_stmt = '''INSERT INTO word_cloud (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES 
                ('COMP101', 'Python Keywords Cloud', 'Contribute to class word cloud', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '3 days', 5, 10, 10, 5), 
                ('ENG101', 'Writing Vocabulary Cloud', 'Add words to our vocabulary cloud', %s, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', 5, 15, 15, 10)''' % (
                    teacher_ids[0], teacher_ids[2]
                )
                db.session.execute(text(word_cloud_stmt))
            else:
                print("Word clouds already exist, skipping...")
            
            # Get word cloud IDs
            result = db.session.execute(text("SELECT id FROM word_cloud ORDER BY id"))
            word_cloud_ids = [row[0] for row in result.fetchall()]
            
            # Load minigames (skip if they exist)
            if existing_counts['minigame'] == 0:
                print("Loading minigames...")
                minigame_stmt = '''INSERT INTO minigame (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, config) VALUES 
                ('COMP101', 'Python Syntax Challenge', 'Interactive syntax matching game', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '7 days', 20, 5, 50, 15, '{"game_type": "syntax_matching", "difficulty": "easy", "time_limit": 300}'), 
                ('COMP201', 'Algorithm Puzzle', 'Solve algorithmic challenges', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '9 days', 30, 3, 75, 20, '{"game_type": "algorithm_puzzle", "difficulty": "medium", "time_limit": 600}')''' % (
                    teacher_ids[0], teacher_ids[0]
                )
                db.session.execute(text(minigame_stmt))
            else:
                print("Minigames already exist, skipping...")
            
            # Get minigame IDs
            result = db.session.execute(text("SELECT id FROM minigame ORDER BY id"))
            minigame_ids = [row[0] for row in result.fetchall()]
            
            # Load questions (skip if they exist)
            if existing_counts['question'] == 0:
                print("Loading questions...")
                question_stmt = '''INSERT INTO question (quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, type, content, points) VALUES 
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
                db.session.execute(text(question_stmt))
            else:
                print("Questions already exist, skipping...")
            
            # Get question IDs
            result = db.session.execute(text("SELECT id FROM question ORDER BY id"))
            question_ids = [row[0] for row in result.fetchall()]
            
            # Load choices (skip if they exist)
            if existing_counts['choice'] == 0:
                print("Loading choices...")
                choice_stmt = '''INSERT INTO choice (question_id, content, is_correct) VALUES 
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
                db.session.execute(text(choice_stmt))
            else:
                print("Choices already exist, skipping...")
            
            # Get choice IDs
            result = db.session.execute(text("SELECT id FROM choice ORDER BY id"))
            choice_ids = [row[0] for row in result.fetchall()]
            
            # Load submissions (skip if they exist)
            if existing_counts['submission'] == 0:
                print("Loading submissions...")
                submission_stmt = '''INSERT INTO submission (user_id, quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, submitted_at, grade) VALUES 
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
                db.session.execute(text(submission_stmt))
            else:
                print("Submissions already exist, skipping...")
            
            # Get submission IDs
            result = db.session.execute(text("SELECT id FROM submission ORDER BY id"))
            submission_ids = [row[0] for row in result.fetchall()]
            
            # Load attempts (skip if they exist)
            if existing_counts['attempt'] == 0:
                print("Loading attempts...")
                attempt_stmt = '''INSERT INTO attempt (quiz_id, user_id, attempt_count, created_at) VALUES 
                (%s, %s, 1, NOW() - INTERVAL '3 hours'),
                (%s, %s, 2, NOW() - INTERVAL '2 hours'),
                (%s, %s, 1, NOW() - INTERVAL '4 hours'),
                (%s, %s, 1, NOW() - INTERVAL '2 hours'),
                (%s, %s, 1, NOW() - INTERVAL '1 hour')''' % (
                    quiz_ids[0], student_ids[0], quiz_ids[0], student_ids[0], quiz_ids[0], student_ids[1], 
                    quiz_ids[1], student_ids[0], quiz_ids[2], student_ids[2]
                )
                db.session.execute(text(attempt_stmt))
            else:
                print("Attempts already exist, skipping...")
            
            # Load question responses - use individual INSERT statements to avoid parameter binding issues
            if existing_counts['question_response'] == 0:
                print("Loading question responses...")
                
                # Insert choice-based responses
                choice_responses = [
                    (submission_ids[0], question_ids[0], choice_ids[1], True, 2.0),
                    (submission_ids[0], question_ids[1], choice_ids[4], True, 2.0),
                    (submission_ids[1], question_ids[3], choice_ids[9], True, 3.0),
                    (submission_ids[1], question_ids[4], choice_ids[14], True, 2.0),
                    (submission_ids[2], question_ids[0], choice_ids[1], True, 2.0),
                    (submission_ids[2], question_ids[1], choice_ids[5], False, 1.0),
                    (submission_ids[3], question_ids[5], choice_ids[17], True, 5.0),
                    (submission_ids[3], question_ids[6], choice_ids[21], True, 3.0),
                    (submission_ids[4], question_ids[7], choice_ids[24], False, 0.0),
                    (submission_ids[5], question_ids[7], choice_ids[25], False, 0.0),
                    (submission_ids[6], question_ids[8], choice_ids[28], False, 0.0),
                    (submission_ids[6], question_ids[9], choice_ids[32], False, 0.0)
                ]
                
                for sub_id, q_id, choice_id, is_correct, points in choice_responses:
                    stmt = f"INSERT INTO question_response (submission_id, question_id, choice_id, is_correct, points) VALUES ({sub_id}, {q_id}, {choice_id}, {is_correct}, {points})"
                    db.session.execute(text(stmt))
                
                # Insert text-based responses
                text_responses = [
                    (submission_ids[0], question_ids[2], 'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)', True, 6.0),
                    (submission_ids[7], question_ids[10], 'The code can be improved by: 1) Adding error handling, 2) Using more descriptive variable names, 3) Adding comments for clarity.', True, 10.0),
                    (submission_ids[7], question_ids[11], 'The time complexity is O(n log n) due to the sorting operation.', True, 10.0),
                    (submission_ids[8], question_ids[12], 'We measured the pendulum period for different lengths and masses.', True, 15.0),
                    (submission_ids[8], question_ids[13], 'The period increased with length but was independent of mass, confirming theoretical predictions.', True, 20.0)
                ]
                
                for sub_id, q_id, text_answer, is_correct, points in text_responses:
                    stmt = f"INSERT INTO question_response (submission_id, question_id, text_answer, is_correct, points) VALUES ({sub_id}, {q_id}, '{text_answer.replace(chr(39), chr(39) + chr(39))}', {is_correct}, {points})"
                    db.session.execute(text(stmt))
            else:
                print("Question responses already exist, skipping...")
            
            # Commit all changes
            db.session.commit()
            print("✓ All data loaded successfully!")
            
            # Final verification
            print("\n=== Final Verification ===")
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
    comprehensive_load()