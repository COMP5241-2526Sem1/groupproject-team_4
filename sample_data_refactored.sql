-- Refactored Sample Data for Educational Management System
-- Updated for Direct Model Architecture (No Polymorphic Inheritance)
-- Each task type (Quiz, Poll, ShortAnswer, WordCloud, Minigame) is independent

-- Level 1: Independent Models

-- Departments
INSERT INTO department (name, full_name) VALUES
('COMP', 'Department of Computer Science'),
('MATH', 'Department of Mathematics'),
('PHYS', 'Department of Physics'),
('CHEM', 'Department of Chemistry'),
('ENG', 'Department of English');

-- Users (Teachers and Students)
-- Note: Using department_code instead of department_id, using String(10) foreign key to department.name
INSERT INTO "user" (username, password_hash, role, email, department_code, created_at) VALUES
-- Teachers
('john_smith', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'teacher', 'john.smith@university.edu', 'COMP', NOW()),
('maria_garcia', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'teacher', 'maria.garcia@university.edu', 'MATH', NOW()),
('david_chen', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'teacher', 'david.chen@university.edu', 'PHYS', NOW()),
-- Students
('alice_johnson', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'alice.j@student.edu', 'COMP', NOW()),
('bob_williams', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'bob.w@student.edu', 'COMP', NOW()),
('carol_davis', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'carol.d@student.edu', 'MATH', NOW()),
('daniel_miller', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'daniel.m@student.edu', 'PHYS', NOW()),
('emma_wilson', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'emma.w@student.edu', 'CHEM', NOW()),
('frank_thomas', 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88', 'student', 'frank.t@student.edu', 'ENG', NOW());

-- Level 2: Courses
-- Note: Using code as primary key, department_code foreign key to department.name, teacher_id foreign key to user.id
INSERT INTO course (code, name, description, department_code, teacher_id, created_at, credit, capacity, day_of_week, start_time, end_time, course_number) VALUES
('COMP101', 'Introduction to Programming', 'Learn Python programming fundamentals', 'COMP', 1, NOW(), 3, 30, 'Mon', '09:00:00', '11:00:00', '101'),
('COMP201', 'Data Structures', 'Advanced data structures and algorithms', 'COMP', 1, NOW(), 3, 25, 'Wed', '14:00:00', '16:00:00', '201'),
('MATH101', 'Calculus I', 'Differential calculus', 'MATH', 2, NOW(), 4, 35, 'Tue', '10:00:00', '12:00:00', '101'),
('PHYS101', 'Physics I', 'Mechanics and thermodynamics', 'PHYS', 3, NOW(), 4, 30, 'Thu', '13:00:00', '15:00:00', '101'),
('ENG101', 'English Composition', 'Academic writing and composition', 'ENG', 3, NOW(), 3, 25, 'Fri', '11:00:00', '13:00:00', '101');

-- Level 3: Independent Task Tables (No Polymorphic Inheritance)
-- Each task type is now completely independent with its own fields

-- Quiz (Standalone table with all required fields)
INSERT INTO quiz (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) VALUES
('COMP101', 'Python Basics Quiz', 'Test your understanding of Python fundamentals', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '7 days', 30, 3, 100, 20, true, false, true, true),
('COMP101', 'Functions and Modules Quiz', 'Assessment on functions and module usage', 1, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', 25, 2, 100, 15, true, true, true, false),
('COMP201', 'Data Structures Quiz', 'Quiz on arrays, lists, and trees', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '10 days', 45, 5, 100, 25, false, true, true, true);

-- Poll (Standalone table with all required fields)
INSERT INTO poll (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) VALUES
('COMP101', 'Course Feedback Poll', 'Help us improve the course', 1, NOW(), NOW() - INTERVAL '3 days', NOW() + INTERVAL '4 days', 15, 1, 0, 0, true, true, true, true),
('MATH101', 'Learning Style Poll', 'What helps you learn best?', 2, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '6 days', 10, 1, 0, 0, true, true, true, true);

-- Short Answer (Standalone table with all required fields)
INSERT INTO short_answer (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES
('COMP101', 'Code Review Assignment', 'Review and improve given code', 1, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '8 days', 60, 1, 100, 30),
('PHYS101', 'Physics Lab Report', 'Write a lab report on pendulum experiment', 3, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '12 days', 120, 1, 100, 35);

-- Word Cloud (Standalone table with all required fields)
INSERT INTO word_cloud (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course) VALUES
('COMP101', 'Python Keywords Cloud', 'Contribute to class word cloud', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '3 days', 5, 10, 10, 5),
('ENG101', 'Writing Vocabulary Cloud', 'Add words to our vocabulary cloud', 3, NOW(), NOW() - INTERVAL '2 days', NOW() + INTERVAL '5 days', 5, 15, 15, 10);

-- Minigame (Standalone table with all required fields)
INSERT INTO minigame (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, config) VALUES
('COMP101', 'Python Syntax Challenge', 'Interactive syntax matching game', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '7 days', 20, 5, 50, 15, '{"game_type": "syntax_matching", "difficulty": "easy", "time_limit": 300}'),
('COMP201', 'Algorithm Puzzle', 'Solve algorithmic challenges', 1, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '9 days', 30, 3, 75, 20, '{"game_type": "algorithm_puzzle", "difficulty": "medium", "time_limit": 600}');

-- Level 4: Course Enrollments
INSERT INTO course_enrollment (course_code, student_id, enrolled_at) VALUES
-- Students enrolled in COMP101
('COMP101', 4, NOW() - INTERVAL '10 days'),
('COMP101', 5, NOW() - INTERVAL '9 days'),
-- Students enrolled in COMP201
('COMP201', 4, NOW() - INTERVAL '8 days'),
-- Students enrolled in MATH101
('MATH101', 6, NOW() - INTERVAL '7 days'),
-- Students enrolled in PHYS101
('PHYS101', 7, NOW() - INTERVAL '6 days'),
-- Students enrolled in ENG101
('ENG101', 8, NOW() - INTERVAL '5 days');

-- Level 5: Questions
-- Note: Each question now links directly to its task type via foreign keys
INSERT INTO question (quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, type, content, points) VALUES
-- Quiz questions
(1, NULL, NULL, NULL, NULL, 'mcq', 'What is the correct way to declare a variable in Python?', 2),
(1, NULL, NULL, NULL, NULL, 'mcq', 'Which of the following is a Python data type?', 2),
(1, NULL, NULL, NULL, NULL, 'saq', 'Write a Python function to calculate the factorial of a number.', 6),
(2, NULL, NULL, NULL, NULL, 'mcq', 'What is the purpose of the "def" keyword in Python?', 3),
(2, NULL, NULL, NULL, NULL, 'mcq', 'How do you import a module in Python?', 2),
(3, NULL, NULL, NULL, NULL, 'mcq', 'What is the time complexity of binary search?', 5),
(3, NULL, NULL, NULL, NULL, 'mcq', 'Which data structure uses LIFO principle?', 3),
-- Poll questions
(NULL, 1, NULL, NULL, NULL, 'mcq', 'How would you rate the course difficulty?', 0),
(NULL, 1, NULL, NULL, NULL, 'mcq', 'What teaching method do you prefer?', 0),
(NULL, 2, NULL, NULL, NULL, 'mcq', 'Do you prefer visual or textual learning materials?', 0),
-- Short Answer questions
(NULL, NULL, 1, NULL, NULL, 'saq', 'Review the provided code and suggest three improvements.', 10),
(NULL, NULL, 1, NULL, NULL, 'saq', 'Explain the time complexity of your suggested solution.', 10),
(NULL, NULL, 2, NULL, NULL, 'saq', 'Describe your pendulum experiment procedure.', 15),
(NULL, NULL, 2, NULL, NULL, 'saq', 'What were your key findings from the experiment?', 20);

-- Level 6: Choices for MCQ questions
INSERT INTO choice (question_id, content, is_correct) VALUES
-- Question 1 choices
(1, 'var x = 5', false),
(1, 'x = 5', true),
(1, 'int x = 5', false),
(1, 'declare x = 5', false),
-- Question 2 choices
(2, 'Integer', true),
(2, 'String', true),
(2, 'Float', true),
(2, 'Character', false),
-- Question 4 choices
(4, 'To declare a variable', false),
(4, 'To define a function', true),
(4, 'To import a module', false),
(4, 'To create a class', false),
-- Question 5 choices
(5, 'include module_name', false),
(5, 'require module_name', false),
(5, 'import module_name', true),
(5, 'using module_name', false),
-- Question 6 choices
(6, 'O(n)', false),
(6, 'O(log n)', true),
(6, 'O(n log n)', false),
(6, 'O(n²)', false),
-- Question 7 choices
(7, 'Queue', false),
(7, 'Stack', true),
(7, 'Array', false),
(7, 'Tree', false),
-- Poll question choices
(8, 'Very Easy', false),
(8, 'Easy', false),
(8, 'Moderate', false),
(8, 'Difficult', false),
(9, 'Lectures only', false),
(9, 'Hands-on practice', false),
(9, 'Group discussions', false),
(9, 'Mixed approach', false),
(10, 'Visual', false),
(10, 'Textual', false),
(10, 'Both equally', false),
(10, 'Depends on topic', false);

-- Level 7: Submissions
-- Note: Each submission links directly to its task type via foreign keys
INSERT INTO submission (user_id, quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, submitted_at, grade) VALUES
-- Quiz submissions
(4, 1, NULL, NULL, NULL, NULL, NOW() - INTERVAL '2 hours', 85.5),
(4, 2, NULL, NULL, NULL, NULL, NOW() - INTERVAL '1 hour', 92.0),
(5, 1, NULL, NULL, NULL, NULL, NOW() - INTERVAL '3 hours', 78.0),
(6, 3, NULL, NULL, NULL, NULL, NOW() - INTERVAL '30 minutes', 88.5),
-- Poll submissions
(4, NULL, 1, NULL, NULL, NULL, NOW() - INTERVAL '1 day', NULL),
(5, NULL, 1, NULL, NULL, NULL, NOW() - INTERVAL '1 day', NULL),
(6, NULL, 2, NULL, NULL, NULL, NOW() - INTERVAL '2 days', NULL),
-- Short answer submissions
(4, NULL, NULL, 1, NULL, NULL, NOW() - INTERVAL '5 hours', 90.0),
(7, NULL, NULL, 2, NULL, NULL, NOW() - INTERVAL '1 day', 85.0);

-- Level 8: Quiz Attempts
INSERT INTO attempt (quiz_id, user_id, attempt_count, created_at) VALUES
(1, 4, 1, NOW() - INTERVAL '3 hours'),
(1, 4, 2, NOW() - INTERVAL '2 hours'),
(1, 5, 1, NOW() - INTERVAL '4 hours'),
(2, 4, 1, NOW() - INTERVAL '2 hours'),
(3, 6, 1, NOW() - INTERVAL '1 hour');

-- Level 9: Question Responses
INSERT INTO question_response (submission_id, question_id, choice_id, text_answer, is_correct, points) VALUES
-- Quiz responses
(1, 1, 2, NULL, true, 2.0),    -- Alice got Q1 correct
(1, 2, 5, NULL, true, 2.0),    -- Alice got Q2 correct (partial)
(1, 3, NULL, 'def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)', true, 6.0),
(2, 4, 10, NULL, true, 3.0),    -- Alice got Q4 correct
(2, 5, 15, NULL, true, 2.0),    -- Alice got Q5 correct
(3, 1, 2, NULL, true, 2.0),     -- Bob got Q1 correct
(3, 2, 6, NULL, false, 1.0),    -- Bob got Q2 partially correct
(4, 6, 18, NULL, true, 5.0),    -- Carol got Q6 correct
(4, 7, 22, NULL, true, 3.0),    -- Carol got Q7 correct
-- Poll responses (no correctness or points)
(5, 8, 25, NULL, false, 0.0),  -- Alice poll response
(5, 9, 29, NULL, false, 0.0),  -- Alice poll response
(6, 8, 26, NULL, false, 0.0),  -- Bob poll response
(6, 9, 30, NULL, false, 0.0),  -- Bob poll response
(7, 10, 33, NULL, false, 0.0),  -- Carol poll response
-- Short answer responses
(8, 11, NULL, 'The code can be improved by: 1) Adding error handling, 2) Using more descriptive variable names, 3) Adding comments for clarity.', true, 10.0),
(8, 12, NULL, 'The time complexity is O(n log n) due to the sorting operation.', true, 10.0),
(9, 13, NULL, 'We measured the pendulum period for different lengths and masses.', true, 15.0),
(9, 14, NULL, 'The period increased with length but was independent of mass, confirming theoretical predictions.', true, 20.0);