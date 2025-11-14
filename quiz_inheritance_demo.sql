-- Demonstration of Quiz model with direct properties (no Task inheritance)
-- This shows how to query Quiz data directly

-- Example 1: Simple query to get Quiz with its properties
SELECT 
    q.id AS quiz_id,
    q.name AS quiz_name,
    q.description AS quiz_description,
    q.duration,
    q.point,
    q.after_submitted_question_visible,
    q.after_submitted_student_response_visible
FROM quiz q
LIMIT 5;

-- Example 2: Get all quizzes with their names and course info
SELECT 
    q.id,
    q.name AS quiz_name,
    c.code AS course_code,
    c.name AS course_name,
    q.start_datetime,
    q.end_datetime,
    q.attempt_limit,
    q.after_submitted_question_visible
FROM quiz q
JOIN course c ON q.course_id = c.id
ORDER BY q.name;

-- Example 3: Count questions for each quiz
SELECT 
    q.id,
    q.name AS quiz_name,
    COUNT(quest.id) AS question_count
FROM quiz q
LEFT JOIN question quest ON q.id = quest.quiz_id
GROUP BY q.id, q.name
ORDER BY question_count DESC;

-- Example 4: Get quiz submissions with quiz names
SELECT 
    s.id AS submission_id,
    u.username,
    q.name AS quiz_name,
    s.grade,
    s.submitted_at
FROM submission s
JOIN quiz q ON s.quiz_id = q.id
JOIN "user" u ON s.user_id = u.id
ORDER BY s.submitted_at DESC;

-- Example 5: Check if a specific ID is a Quiz
SELECT 
    q.id,
    q.name,
    'Yes, this is a Quiz' AS is_quiz
FROM quiz q
WHERE q.id = 1;  -- Change this ID to test different quizzes