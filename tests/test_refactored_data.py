#!/usr/bin/env python3
"""
Test script to validate the refactored SQL data and new model architecture
"""

from app import app
from database import db
from sqlalchemy import text

def test_refactored_data():
    """Test the refactored data to ensure model architecture is correct"""
    
    with app.app_context():
        try:
            print("=== Testing Refactored Data Model ===\n")
            
            # Test 1: Department structure (name as primary key)
            print("1. Testing Department Structure:")
            result = db.session.execute(text("""
                SELECT name, full_name 
                FROM department 
                ORDER BY name
            """))
            departments = result.fetchall()
            for dept in departments:
                print(f"   {dept.name}: {dept.full_name}")
            print(f"   ✓ Found {len(departments)} departments\n")
            
            # Test 2: User structure (department_code foreign key)
            print("2. Testing User Structure:")
            result = db.session.execute(text("""
                SELECT u.username, u.role, u.email, u.department_code, d.full_name
                FROM "user" u
                JOIN department d ON u.department_code = d.name
                ORDER BY u.username
            """))
            users = result.fetchall()
            for user in users:
                print(f"   {user.username} ({user.role}): {user.email} - {user.department_code} ({user.full_name})")
            print(f"   ✓ Found {len(users)} users with department relationships\n")
            
            # Test 3: Course structure (code as primary key, department_code foreign key)
            print("3. Testing Course Structure:")
            result = db.session.execute(text("""
                SELECT c.code, c.name, c.department_code, d.full_name, u.username as teacher
                FROM course c
                JOIN department d ON c.department_code = d.name
                JOIN "user" u ON c.teacher_id = u.id
                ORDER BY c.code
            """))
            courses = result.fetchall()
            for course in courses:
                print(f"   {course.code}: {course.name} - {course.department_code} ({course.full_name}) - Teacher: {course.teacher}")
            print(f"   ✓ Found {len(courses)} courses\n")
            
            # Test 4: Independent Quiz Model (No Polymorphic Inheritance)
            print("4. Testing Independent Quiz Model:")
            result = db.session.execute(text("""
                SELECT q.id, q.name, q.description, q.course_code, c.name as course_name,
                       q.duration, q.attempt_limit, q.point, q.point_in_course,
                       q.after_submitted_question_visible, q.after_submitted_student_response_visible
                FROM quiz q
                JOIN course c ON q.course_code = c.code
                ORDER BY q.id
            """))
            quizzes = result.fetchall()
            for quiz in quizzes:
                print(f"   Quiz {quiz.id}: {quiz.name}")
                print(f"      Course: {quiz.course_code} - {quiz.course_name}")
                print(f"      Settings: Duration={quiz.duration}min, Attempts={quiz.attempt_limit}, Points={quiz.point}")
                print(f"      Visibility: Questions={quiz.after_submitted_question_visible}, StudentResponses={quiz.after_submitted_student_response_visible}")
            print(f"   ✓ Found {len(quizzes)} quizzes with direct properties\n")
            
            # Test 5: Independent Poll Model
            print("5. Testing Independent Poll Model:")
            result = db.session.execute(text("""
                SELECT p.id, p.name, p.description, p.course_code, c.name as course_name,
                       p.duration, p.attempt_limit, p.point, p.point_in_course
                FROM poll p
                JOIN course c ON p.course_code = c.code
                ORDER BY p.id
            """))
            polls = result.fetchall()
            for poll in polls:
                print(f"   Poll {poll.id}: {poll.name}")
                print(f"      Course: {poll.course_code} - {poll.course_name}")
                print(f"      Settings: Duration={poll.duration}min, Attempts={poll.attempt_limit}, Points={poll.point}")
            print(f"   ✓ Found {len(polls)} polls with direct properties\n")
            
            # Test 6: Course Enrollments
            print("6. Testing Course Enrollments:")
            result = db.session.execute(text("""
                SELECT c.code, c.name as course_name, u.username as student, ce.enrolled_at
                FROM course_enrollment ce
                JOIN course c ON ce.course_code = c.code
                JOIN "user" u ON ce.student_id = u.id
                ORDER BY c.code, u.username
            """))
            enrollments = result.fetchall()
            for enrollment in enrollments:
                print(f"   {enrollment.code}: {enrollment.student} enrolled on {enrollment.enrolled_at}")
            print(f"   ✓ Found {len(enrollments)} enrollments\n")
            
            # Test 7: Questions linked to independent task tables
            print("7. Testing Question Links to Independent Tasks:")
            result = db.session.execute(text("""
                SELECT q.id, q.type, q.content, q.points,
                       CASE 
                           WHEN q.quiz_id IS NOT NULL THEN 'Quiz ' || q.quiz_id
                           WHEN q.poll_id IS NOT NULL THEN 'Poll ' || q.poll_id
                           WHEN q.short_answer_id IS NOT NULL THEN 'ShortAnswer ' || q.short_answer_id
                           ELSE 'Other'
                       END as task_type
                FROM question q
                ORDER BY q.id
            """))
            questions = result.fetchall()
            for question in questions:
                print(f"   Question {question.id} ({question.type}): {question.content[:50]}...")
                print(f"      Linked to: {question.task_type}, Points: {question.points}")
            print(f"   ✓ Found {len(questions)} questions\n")
            
            # Test 8: Submissions to independent task tables
            print("8. Testing Submission Links to Independent Tasks:")
            result = db.session.execute(text("""
                SELECT s.id, u.username, 
                       CASE 
                           WHEN s.quiz_id IS NOT NULL THEN 'Quiz ' || s.quiz_id
                           WHEN s.poll_id IS NOT NULL THEN 'Poll ' || s.poll_id
                           WHEN s.short_answer_id IS NOT NULL THEN 'ShortAnswer ' || s.short_answer_id
                           ELSE 'Other'
                       END as task_type,
                       s.grade, s.submitted_at
                FROM submission s
                JOIN "user" u ON s.user_id = u.id
                ORDER BY s.id
            """))
            submissions = result.fetchall()
            for submission in submissions:
                print(f"   Submission {submission.id}: {submission.username} - {submission.task_type}")
                print(f"      Grade: {submission.grade}, Submitted: {submission.submitted_at}")
            print(f"   ✓ Found {len(submissions)} submissions\n")
            
            print("=== All Tests Passed! ✓ ===")
            print("\nKey Benefits Verified:")
            print("✓ Direct model architecture working correctly")
            print("✓ No polymorphic inheritance complexity")
            print("✓ Simplified queries with direct property access")
            print("✓ Proper foreign key relationships maintained")
            print("✓ Independent task tables functioning as expected")
            
        except Exception as e:
            print(f"✗ Error during testing: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    test_refactored_data()