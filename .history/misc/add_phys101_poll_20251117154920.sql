-- Add PHYS101 Poll with Questions and Choices for testing
INSERT INTO poll (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) 
VALUES ('PHYS101', 'Physics Understanding Poll', 'Test your understanding of key physics concepts', 3, NOW(), NOW() - INTERVAL '1 day', NOW() + INTERVAL '10 days', 20, 2, 0, 0, true, true, true, true);

-- Get the ID of the newly created poll (will be 3 if first two are in COMP101 and MATH101)
-- Insert Questions for this poll
INSERT INTO question (poll_id, type, content, points) 
VALUES 
(3, 'mcq', '物理学中力的基本定义是什么？', 0),
(3, 'mcq', '能量守恒定律指出什么？', 0),
(3, 'mcq', '热力学第二定律在日常生活中的应用是什么？', 0);

-- Insert Choices for Question 1
INSERT INTO choice (question_id, content, is_correct) 
VALUES 
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%力的基本定义%' LIMIT 1), '物体在单位时间内的质量变化', false),
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%力的基本定义%' LIMIT 1), '单位质量受到的加速度', false),
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%力的基本定义%' LIMIT 1), '作用在物体上，使其改变运动状态的原因', true),
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%力的基本定义%' LIMIT 1), '物体克服摩擦力所做的功', false);

-- Insert Choices for Question 2
INSERT INTO choice (question_id, content, is_correct) 
VALUES 
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%能量守恒定律%' LIMIT 1), '能量可以被创造和销毁', false),
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%能量守恒定律%' LIMIT 1), '能量既不能创造也不能销毁，只能转换', true),
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%能量守恒定律%' LIMIT 1), '能量总是减少的', false),
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%能量守恒定律%' LIMIT 1), '能量总是增加的', false);

-- Insert Choices for Question 3
INSERT INTO choice (question_id, content, is_correct) 
VALUES 
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%热力学第二定律%' LIMIT 1), '冰箱制冷保持食物新鲜', true),
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%热力学第二定律%' LIMIT 1), '热水自动冷却到室温', true),
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%热力学第二定律%' LIMIT 1), '电灯发光发热', false),
((SELECT id FROM question WHERE poll_id = 3 AND content LIKE '%热力学第二定律%' LIMIT 1), '水从高处流向低处', false);
