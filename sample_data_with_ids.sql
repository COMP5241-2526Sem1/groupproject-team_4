-- Sample Data for Educational Management System with Explicit IDs
-- Generated based on model dependencies analysis with specific IDs

-- Level 1: Independent Models

-- Departments
INSERT INTO department (id, name, full_name) VALUES
(1, 'COMP', 'Department of Computer Science'),
(2, 'MATH', 'Department of Mathematics'),
(3, 'PHYS', 'Department of Physics'),
(4, 'CHEM', 'Department of Chemistry'),
(5, 'ENG', 'Department of English');

-- Users (Teachers and Students)
INSERT INTO "user" (id, username, password_hash, role, email, department_id, created_at) VALUES
-- Teachers
(1, 'john_smith', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'teacher', 'john.smith@university.edu', 1, NOW()),
(2, 'maria_garcia', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'teacher', 'maria.garcia@university.edu', 2, NOW()),
(3, 'david_chen', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'teacher', 'david.chen@university.edu', 3, NOW()),
-- Students
(4, 'alice_johnson', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'alice.j@student.edu', 1, NOW()),
(5, 'bob_williams', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'bob.w@student.edu', 1, NOW()),
(6, 'carol_davis', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'carol.d@student.edu', 2, NOW()),
(7, 'daniel_miller', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'daniel.m@student.edu', 3, NOW()),
(8, 'emma_wilson', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'emma.w@student.edu', 4, NOW()),
(9, 'frank_thomas', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'frank.t@student.edu', 5, NOW());

-- Level 2: Courses

INSERT INTO course (id, code, name, description, department_id, teacher_id, created_at, credit, capacity, day_of_week, start_time, end_time) VALUES
(1, 'COMP101', 'Introduction to Programming', 'Learn fundamental programming concepts using Python', 1, 1, NOW(), 3, 30, 'Mon', '09:00:00', '11:00:00'),
(2, 'COMP201', 'Data Structures', 'Advanced data structures and algorithms', 1, 1, NOW(), 3, 25, 'Wed', '14:00:00', '16:00:00'),
(3, 'MATH101', 'Calculus I', 'Differential calculus fundamentals', 2, 2, NOW(), 4, 35, 'Tue', '10:00:00', '12:00:00'),
(4, 'PHYS101', 'Physics I', 'Mechanics and thermodynamics', 3, 3, NOW(), 4, 28, 'Thu', '13:00:00', '15:00:00'),
(5, 'ENG101', 'English Composition', 'Academic writing and communication', 5, 4, NOW(), 3, 20, 'Fri', '11:00:00', '13:00:00');

-- Level 3: Tasks (Base tasks for inheritance)

INSERT INTO quiz (id, course_id, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES
(1, 1, 'Python Basics Quiz', 'Test your understanding of Python fundamentals', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '7 days', 30, 3, 100, 20),
(2, 1, 'Functions and Modules Quiz', 'Assessment on functions and module usage', 1, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', 25, 2, 100, 15),
(3, 2, 'Data Structures Quiz', 'Quiz on arrays, lists, and trees', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '10 days', 45, 5, 100, 25);

INSERT INTO poll (id, course_id, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES
(4, 1, 'Course Feedback Poll', 'Help us improve the course', 1, NOW(), NOW() - INTERVAL '3 days', NOW() + INTERVAL '4 days', 15, 1, 0, 0),
(5, 3, 'Learning Style Poll', 'What helps you learn best?', 2, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '6 days', 10, 1, 0, 0);

INSERT INTO short_answer (id, course_id, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES
(6, 1, 'Code Review Assignment', 'Review and improve given code', 1, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '8 days', 60, 1, 100, 30),
(7, 4, 'Physics Lab Report', 'Write a lab report on pendulum experiment', 3, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '12 days', 120, 1, 100, 35);

INSERT INTO word_cloud (id, course_id, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES
(8, 1, 'Python Keywords Cloud', 'Contribute to class word cloud', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '3 days', 5, 10, 10, 5),
(9, 5, 'Writing Vocabulary Cloud', 'Add words to our vocabulary cloud', 4, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', 5, 15, 15, 10);

INSERT INTO minigame (id, course_id, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES
(10, 1, 'Python Syntax Challenge', 'Interactive syntax matching game', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '7 days', 20, 5, 50, 15),
(11, 2, 'Algorithm Puzzle', 'Solve algorithmic challenges', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '9 days', 30, 3, 75, 20);

-- Level 4: Task-specific data (Quiz, Poll, etc.)

-- Quiz-specific settings
INSERT INTO quiz (id, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) VALUES
(1, true, false, true, true),
(2, true, true, true, false),
(3, false, true, true, true);

-- Poll-specific settings (no additional fields needed)
-- Short Answer-specific settings (no additional fields needed)
-- Word Cloud-specific settings (no additional fields needed)
-- Minigame-specific settings
INSERT INTO minigame (id, config) VALUES
(10, '{"game_type": "syntax_matching", "difficulty": "easy", "time_limit": 300}'),
(11, '{"game_type": "algorithm_puzzle", "difficulty": "medium", "time_limit": 600}');

-- Level 5: Course Enrollments

INSERT INTO course_enrollment (id, course_id, student_id, enrolled_at) VALUES
-- Students enrolled in COMP101
(1, 1, 4, NOW() - INTERVAL '10 days'),
(2, 1, 5, NOW() - INTERVAL '9 days'),
-- Students enrolled in COMP201
(3, 2, 4, NOW() - INTERVAL '8 days'),
-- Students enrolled in MATH101
(4, 3, 6, NOW() - INTERVAL '7 days'),
-- Students enrolled in PHYS101
(5, 4, 7, NOW() - INTERVAL '6 days'),
-- Students enrolled in ENG101
(6, 5, 8, NOW() - INTERVAL '5 days');

-- Level 6: Questions

INSERT INTO question (id, quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, type, content, points) VALUES
-- Quiz questions
(1, 1, NULL, NULL, NULL, NULL, 'mcq', 'What is the correct way to declare a variable in Python?', 2),
(2, 1, NULL, NULL, NULL, NULL, 'mcq', 'Which of the following is a Python data type?', 2),
(3, 1, NULL, NULL, NULL, NULL, 'saq', 'Write a Python function to calculate the factorial of a number.', 6),
(4, 2, NULL, NULL, NULL, NULL, 'mcq', 'What is the purpose of the "def" keyword in Python?', 3),
(5, 2, NULL, NULL, NULL, NULL, 'mcq', 'How do you import a module in Python?', 2),
(6, 3, NULL, NULL, NULL, NULL, 'mcq', 'What is the time complexity of binary search?', 5),
(7, 3, NULL, NULL, NULL, NULL, 'mcq', 'Which data structure uses LIFO principle?', 3),
-- Poll questions
(8, NULL, 4, NULL, NULL, NULL, 'mcq', 'How would you rate the course difficulty?', 0),
(9, NULL, 4, NULL, NULL, NULL, 'mcq', 'What teaching method do you prefer?', 0),
(10, NULL, 5, NULL, NULL, NULL, 'mcq', 'Do you prefer visual or textual learning materials?', 0),
-- Short Answer questions
(11, NULL, NULL, 6, NULL, NULL, 'saq', 'Review the provided code and suggest three improvements.', 10),
(12, NULL, NULL, 6, NULL, NULL, 'saq', 'Explain the time complexity of your suggested solution.', 10),
(13, NULL, NULL, 7, NULL, NULL, 'saq', 'Describe your pendulum experiment procedure.', 15),
(14, NULL, NULL, 7, NULL, NULL, 'saq', 'What were your key findings from the experiment?', 20);

-- Level 7: Choices for MCQ questions

INSERT INTO choice (id, question_id, content, is_correct) VALUES
-- Question 1 choices
(1, 1, 'var x = 5', false),
(2, 1, 'x = 5', true),
(3, 1, 'int x = 5', false),
(4, 1, 'declare x = 5', false),
-- Question 2 choices
(5, 2, 'Integer', true),
(6, 2, 'String', true),
(7, 2, 'Float', true),
(8, 2, 'Character', false),
-- Question 4 choices
(9, 4, 'To declare a variable', false),
(10, 4, 'To define a function', true),
(11, 4, 'To import a module', false),
(12, 4, 'To create a class', false),
-- Question 5 choices
(13, 5, 'include module_name', false),
(14, 5, 'require module_name', false),
(15, 5, 'import module_name', true),
(16, 5, 'using module_name', false),
-- Question 6 choices
(17, 6, 'O(n)', false),
(18, 6, 'O(log n)', true),
(19, 6, 'O(n log n)', false),
(20, 6, 'O(n²)', false),
-- Question 7 choices
(21, 7, 'Queue', false),
(22, 7, 'Stack', true),
(23, 7, 'Array', false),
(24, 7, 'Tree', false),
-- Poll question choices
(25, 8, 'Very Easy', false),
(26, 8, 'Easy', false),
(27, 8, 'Moderate', false),
(28, 8, 'Difficult', false),
(29, 9, 'Lectures only', false),
(30, 9, 'Hands-on practice', false),
(31, 9, 'Group discussions', false),
(32, 9, 'Mixed approach', false),
(33, 10, 'Visual', false),
(34, 10, 'Textual', false),
(35, 10, 'Both equally', false),
(36, 10, 'Depends on topic', false);

-- Level 8: Submissions

INSERT INTO submission (id, user_id, quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, submitted_at, grade) VALUES
-- Quiz submissions
(1, 4, 1, NULL, NULL, NULL, NULL, NOW() - INTERVAL '2 hours', 85.5),
(2, 4, 2, NULL, NULL, NULL, NULL, NOW() - INTERVAL '1 hour', 92.0),
(3, 5, 1, NULL, NULL, NULL, NULL, NOW() - INTERVAL '3 hours', 78.0),
(4, 6, 3, NULL, NULL, NULL, NULL, NOW() - INTERVAL '30 minutes', 88.5),
-- Poll submissions
(5, 4, NULL, 4, NULL, NULL, NULL, NOW() - INTERVAL '1 day', NULL),
(6, 5, NULL, 4, NULL, NULL, NULL, NOW() - INTERVAL '1 day', NULL),
(7, 6, NULL, 5, NULL, NULL, NULL, NOW() - INTERVAL '2 days', NULL),
-- Short answer submissions
(8, 4, NULL, NULL, 6, NULL, NULL, NOW() - INTERVAL '5 hours', 90.0),
(9, 7, NULL, NULL, 7, NULL, NULL, NOW() - INTERVAL '1 day', 85.0);

-- Level 9: Quiz Attempts

INSERT INTO attempt (id, quiz_id, user_id, attempt_count, created_at) VALUES
(1, 1, 4, 1, NOW() - INTERVAL '3 hours'),
(2, 1, 4, 2, NOW() - INTERVAL '2 hours'),
(3, 1, 5, 1, NOW() - INTERVAL '4 hours'),
(4, 2, 4, 1, NOW() - INTERVAL '2 hours'),
(5, 3, 6, 1, NOW() - INTERVAL '1 hour');

-- Level 10: Question Responses

INSERT INTO question_response (id, submission_id, question_id, choice_id, text_answer, is_correct, points) VALUES
-- Quiz responses
(1, 1, 1, 2, NULL, true, 2.0),    -- Alice got Q1 correct
(2, 1, 2, 5, NULL, true, 2.0),    -- Alice got Q2 correct (partial)
(3, 1, 3, NULL, 'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)', true, 6.0),
(4, 2, 4, 10, NULL, true, 3.0),    -- Alice got Q4 correct
(5, 2, 5, 15, NULL, true, 2.0),    -- Alice got Q5 correct
(6, 3, 1, 2, NULL, true, 2.0),     -- Bob got Q1 correct
(7, 3, 2, 6, NULL, false, 1.0),    -- Bob got Q2 partially correct
(8, 4, 6, 18, NULL, true, 5.0),    -- Carol got Q6 correct
(9, 4, 7, 22, NULL, true, 3.0),    -- Carol got Q7 correct
-- Poll responses (no correctness or points)
(10, 5, 8, 25, NULL, false, 0.0),  -- Alice poll response
(11, 5, 9, 29, NULL, false, 0.0),  -- Alice poll response
(12, 6, 8, 26, NULL, false, 0.0),  -- Bob poll response
(13, 6, 9, 30, NULL, false, 0.0),  -- Bob poll response
(14, 7, 10, 33, NULL, false, 0.0),  -- Carol poll response
-- Short answer responses
(15, 8, 11, NULL, 'The code can be improved by: 1) Adding error handling, 2) Using more descriptive variable names, 3) Adding comments for clarity.', true, 10.0),
(16, 8, 12, NULL, 'The time complexity is O(n log n) due to the sorting operation.', true, 10.0),
(17, 9, 13, NULL, 'We measured the period of a simple pendulum by timing 10 oscillations and calculating the average.', true, 15.0),
(18, 9, 14, NULL, 'Our findings showed that the period is independent of mass and amplitude, confirming the theoretical model.', true, 20.0);

-- Level 11: Word Cloud Entries

INSERT INTO word_entry (id, word_cloud_id, word, frequency, submitted_by, submitted_at) VALUES
-- Python Keywords Cloud entries
(1, 8, 'function', 5, 4, NOW() - INTERVAL '2 days'),
(2, 8, 'variable', 4, 4, NOW() - INTERVAL '2 days'),
(3, 8, 'loop', 6, 5, NOW() - INTERVAL '1 day'),
(4, 8, 'list', 3, 5, NOW() - INTERVAL '1 day'),
(5, 8, 'dictionary', 2, 4, NOW() - INTERVAL '12 hours'),
-- Writing Vocabulary Cloud entries
(6, 9, 'thesis', 4, 8, NOW() - INTERVAL '3 days'),
(7, 9, 'argument', 3, 8, NOW() - INTERVAL '3 days'),
(8, 9, 'evidence', 5, 8, NOW() - INTERVAL '2 days'),
(9, 9, 'conclusion', 2, 8, NOW() - INTERVAL '1 day');

-- Level 12: Minigame Sessions

INSERT INTO minigame_session (id, game_id, user_id, score, state, started_at, completed_at) VALUES
(1, 10, 4, 850, '{"level": 3, "lives": 2, "completed": true}', NOW() - INTERVAL '4 hours', NOW() - INTERVAL '3 hours'),
(2, 10, 5, 720, '{"level": 2, "lives": 1, "completed": true}', NOW() - INTERVAL '2 hours', NOW() - INTERVAL '1 hour'),
(3, 11, 4, 1200, '{"puzzles_solved": 5, "time_bonus": 200, "completed": true}', NOW() - INTERVAL '1 day', NOW() - INTERVAL '20 hours'),
(4, 11, 6, 980, '{"puzzles_solved": 4, "time_bonus": 180, "completed": true}', NOW() - INTERVAL '2 days', NOW() - INTERVAL '1 day');

-- Level 13: Final Grades

INSERT INTO grade (id, course_id, student_id, grade, updated_at) VALUES
-- Final course grades
(1, 1, 4, 87.5, NOW()),  -- Alice in COMP101
(2, 1, 5, 79.0, NOW()),  -- Bob in COMP101
(3, 2, 4, 91.0, NOW()),  -- Alice in COMP201
(4, 3, 6, 88.5, NOW()),  -- Carol in MATH101
(5, 4, 7, 85.0, NOW()),  -- Daniel in PHYS101
(6, 5, 8, 92.0, NOW());  -- Emma in ENG101

-- Additional sample data for more comprehensive testing

-- More departments
INSERT INTO department (id, name, full_name) VALUES
(6, 'BIO', 'Department of Biology'),
(7, 'HIST', 'Department of History'),
(8, 'ECON', 'Department of Economics');

-- More courses
INSERT INTO course (id, code, name, description, department_id, teacher_id, created_at, credit, capacity, day_of_week, start_time, end_time) VALUES
(6, 'BIO101', 'General Biology', 'Introduction to biological sciences', 6, 2, NOW(), 4, 30, 'Mon', '14:00:00', '16:00:00'),
(7, 'HIST101', 'World History', 'Survey of world civilizations', 7, 3, NOW(), 3, 25, 'Wed', '09:00:00', '11:00:00'),
(8, 'ECON101', 'Microeconomics', 'Principles of microeconomics', 8, 1, NOW(), 3, 28, 'Fri', '14:00:00', '16:00:00');

-- More complex quiz with various question types
INSERT INTO quiz (id, course_id, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) VALUES
(12, 1, 'Comprehensive Python Assessment', 'Final assessment covering all Python topics', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '14 days', 60, 2, 200, 40, true, true, true, true);

-- Add questions for comprehensive assessment
INSERT INTO question (id, quiz_id, type, content, points) VALUES
(15, 12, 'mcq', 'Which Python data structure is best for storing key-value pairs?', 3),
(16, 12, 'mcq', 'What does the "len()" function return for a string?', 2),
(17, 12, 'saq', 'Explain the difference between a list and a tuple in Python.', 8),
(18, 12, 'mcq', 'Which exception is raised when trying to access a non-existent dictionary key?', 4),
(19, 12, 'saq', 'Write a function that finds the largest number in a list.', 10);

-- Add choices for new questions
INSERT INTO choice (id, question_id, content, is_correct) VALUES
(37, 15, 'List', false),
(38, 15, 'Tuple', false),
(39, 15, 'Dictionary', true),
(40, 15, 'Set', false),
(41, 16, 'The first character', false),
(42, 16, 'The number of characters', true),
(43, 16, 'The ASCII value', false),
(44, 16, 'An error', false),
(45, 18, 'ValueError', false),
(46, 18, 'KeyError', true),
(47, 18, 'IndexError', false),
(48, 18, 'TypeError', false);

-- Add more submissions and responses
INSERT INTO submission (id, user_id, quiz_id, submitted_at, grade) VALUES
(10, 4, 12, NOW() - INTERVAL '2 hours', 178.5),
(11, 5, 12, NOW() - INTERVAL '1 hour', 165.0);

INSERT INTO question_response (id, submission_id, question_id, choice_id, text_answer, is_correct, points) VALUES
(19, 10, 15, 39, NULL, true, 3.0),
(20, 10, 16, 42, NULL, true, 2.0),
(21, 10, 17, NULL, 'Lists are mutable and can be changed after creation, while tuples are immutable and cannot be modified once created.', true, 8.0),
(22, 10, 18, 46, NULL, true, 4.0),
(23, 10, 19, NULL, 'def find_largest(numbers):\n    if not numbers:\n        return None\n    largest = numbers[0]\n    for num in numbers[1:]:\n        if num > largest:\n            largest = num\n    return largest', true, 10.0),
(24, 11, 15, 39, NULL, true, 3.0),
(25, 11, 16, 43, NULL, false, 0.0),
(26, 11, 17, NULL, 'Lists can be modified, tuples cannot.', true, 6.0),
(27, 11, 18, 45, NULL, false, 0.0),
(28, 11, 19, NULL, 'max(list)', true, 8.0);

-- Add more attempts
INSERT INTO attempt (id, quiz_id, user_id, attempt_count, created_at) VALUES
(6, 12, 4, 1, NOW() - INTERVAL '3 hours'),
(7, 12, 5, 1, NOW() - INTERVAL '2 hours');

-- Add more word cloud entries
INSERT INTO word_entry (id, word_cloud_id, word, frequency, submitted_by, submitted_at) VALUES
(10, 8, 'class', 3, 5, NOW() - INTERVAL '6 hours'),
(11, 8, 'method', 2, 4, NOW() - INTERVAL '4 hours'),
(12, 9, 'analysis', 4, 8, NOW() - INTERVAL '1 day'),
(13, 9, 'research', 3, 8, NOW() - INTERVAL '12 hours');

-- Add more minigame sessions
INSERT INTO minigame_session (id, game_id, user_id, score, state, started_at, completed_at) VALUES
(5, 10, 6, 650, '{"level": 2, "lives": 0, "completed": false}', NOW() - INTERVAL '6 hours', NOW() - INTERVAL '5 hours'),
(6, 11, 7, 1100, '{"puzzles_solved": 4, "time_bonus": 150, "completed": true}', NOW() - INTERVAL '3 days', NOW() - INTERVAL '2 days');

-- Add final grades for additional courses
INSERT INTO grade (id, course_id, student_id, grade, updated_at) VALUES
(7, 6, 4, 89.0, NOW()),  -- Alice in BIO101
(8, 7, 7, 86.5, NOW()),  -- Daniel in HIST101
(9, 8, 5, 91.5, NOW());  -- Bob in ECON101