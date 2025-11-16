#!/usr/bin/env python3
"""
Fix SQL statements and load them properly
"""

from app import app
from database import db
from sqlalchemy import text

def fix_and_load_sql():
    """Fix SQL statements and load them"""
    
    with app.app_context():
        try:
            print("=== Fixing and Loading SQL ===")
            
            # Load departments first
            dept_stmt = "INSERT INTO department (name, full_name) VALUES ('COMP', 'Department of Computer Science'), ('MATH', 'Department of Mathematics'), ('PHYS', 'Department of Physics'), ('CHEM', 'Department of Chemistry'), ('ENG', 'Department of English')"
            print("Loading departments...")
            db.session.execute(text(dept_stmt))
            
            # Load users
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
            print("Loading users...")
            db.session.execute(text(user_stmt))
            
            # Get the actual user IDs
            result = db.session.execute(text("SELECT id, username FROM \"user\" ORDER BY id"))
            users = result.fetchall()
            print("Users loaded:")
            for user in users:
                print(f"  ID {user[0]}: {user[1]}")
            
            # Load courses with correct teacher IDs
            course_stmt = '''INSERT INTO course (code, name, description, department_code, teacher_id, created_at, credit, capacity, day_of_week, start_time, end_time, course_number) VALUES 
            ('COMP101', 'Introduction to Programming', 'Learn Python programming fundamentals', 'COMP', %s, NOW(), 3, 30, 'Mon', '09:00:00', '11:00:00', '101'), 
            ('COMP201', 'Data Structures', 'Advanced data structures and algorithms', 'COMP', %s, NOW(), 3, 25, 'Wed', '14:00:00', '16:00:00', '201'), 
            ('MATH101', 'Calculus I', 'Differential calculus', 'MATH', %s, NOW(), 4, 35, 'Tue', '10:00:00', '12:00:00', '101'), 
            ('PHYS101', 'Physics I', 'Mechanics and thermodynamics', 'PHYS', %s, NOW(), 4, 30, 'Thu', '13:00:00', '15:00:00', '101'), 
            ('ENG101', 'English Composition', 'Academic writing and composition', 'ENG', %s, NOW(), 3, 25, 'Fri', '11:00:00', '13:00:00', '101')''' % (
                users[0][0], users[1][0], users[1][0], users[2][0], users[2][0]
            )
            print("Loading courses...")
            db.session.execute(text(course_stmt))
            
            # Load the rest of the data
            other_statements = [
                '''INSERT INTO quiz (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) VALUES 
                ('COMP101', 'Python Basics Quiz', 'Test your understanding of Python fundamentals', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '7 days', 30, 3, 100, 20, true, false, true, true), 
                ('COMP101', 'Functions and Modules Quiz', 'Assessment on functions and module usage', %s, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', 25, 2, 100, 15, true, true, true, false), 
                ('COMP201', 'Data Structures Quiz', 'Quiz on arrays, lists, and trees', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '10 days', 45, 5, 100, 25, false, true, true, true)''' % (users[0][0], users[0][0], users[0][0]),
                
                '''INSERT INTO poll (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) VALUES 
                ('COMP101', 'Course Feedback Poll', 'Help us improve the course', %s, NOW(), NOW() - INTERVAL '3 days', NOW() + INTERVAL '4 days', 15, 1, 0, 0, true, true, true, true), 
                ('MATH101', 'Learning Style Poll', 'What helps you learn best?', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '6 days', 10, 1, 0, 0, true, true, true, true)''' % (users[0][0], users[1][0]),
                
                '''INSERT INTO short_answer (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES 
                ('COMP101', 'Code Review Assignment', 'Review and improve given code', %s, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '8 days', 60, 1, 100, 30), 
                ('PHYS101', 'Physics Lab Report', 'Write a lab report on pendulum experiment', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '12 days', 120, 1, 100, 35)''' % (users[0][0], users[2][0]),
                
                '''INSERT INTO word_cloud (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES 
                ('COMP101', 'Python Keywords Cloud', 'Contribute to class word cloud', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '3 days', 5, 10, 10, 5), 
                ('ENG101', 'Writing Vocabulary Cloud', 'Add words to our vocabulary cloud', %s, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', 5, 15, 15, 10)''' % (users[0][0], users[2][0]),
                
                '''INSERT INTO minigame (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, config) VALUES 
                ('COMP101', 'Python Syntax Challenge', 'Interactive syntax matching game', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '7 days', 20, 5, 50, 15, '{"game_type": "syntax_matching", "difficulty": "easy", "time_limit": 300}'), 
                ('COMP201', 'Algorithm Puzzle', 'Solve algorithmic challenges', %s, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '9 days', 30, 3, 75, 20, '{"game_type": "algorithm_puzzle", "difficulty": "medium", "time_limit": 600}')''' % (users[0][0], users[0][0]),
                
                '''INSERT INTO course_enrollment (course_code, student_id, enrolled_at) VALUES 
                ('COMP101', %s, NOW() - INTERVAL '10 days'), 
                ('COMP101', %s, NOW() - INTERVAL '9 days'), 
                ('COMP201', %s, NOW() - INTERVAL '8 days'), 
                ('MATH101', %s, NOW() - INTERVAL '7 days'), 
                ('PHYS101', %s, NOW() - INTERVAL '6 days'), 
                ('ENG101', %s, NOW() - INTERVAL '5 days')''' % (users[3][0], users[4][0], users[3][0], users[5][0], users[6][0], users[7][0])
            ]
            
            # Execute remaining statements
            for i, stmt in enumerate(other_statements):
                print(f"Executing additional statement {i+1}...")
                db.session.execute(text(stmt))
            
            # Commit all changes
            db.session.commit()
            print("✓ All data loaded successfully!")
            
            # Verify data was loaded
            tables = ['department', 'course', 'quiz', 'poll', 'short_answer', 'word_cloud', 'minigame', 'course_enrollment', 'question', 'choice', 'submission', 'attempt', 'question_response']
            
            for table in tables:
                try:
                    result = db.session.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"{table}: {count}")
                except Exception as e:
                    print(f"{table}: Error counting - {e}")
                    
        except Exception as e:
            print(f"✗ Failed to load data: {e}")
            db.session.rollback()
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    fix_and_load_sql()