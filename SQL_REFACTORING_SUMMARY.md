# SQL Insert Statements Refactoring Summary

## Overview
The SQL insert statements have been refactored to align with the new **direct model architecture** that eliminates polymorphic inheritance. Each task type (Quiz, Poll, ShortAnswer, WordCloud, Minigame) is now completely independent.

## Key Changes Made

### 1. **Department Table Changes**
**Before:**
```sql
INSERT INTO department (id, name, full_name) VALUES
(1, 'COMP', 'Department of Computer Science'),
```

**After:**
```sql
INSERT INTO department (name, full_name) VALUES
('COMP', 'Department of Computer Science'),
```
- **Removed:** Auto-increment `id` field
- **Changed:** `name` is now the primary key (department code)

### 2. **User Table Changes**
**Before:**
```sql
INSERT INTO "user" (id, username, password_hash, role, email, department_id, created_at) VALUES
(1, 'john_smith', '...', 'teacher', 'john.smith@university.edu', 1, NOW()),
```

**After:**
```sql
INSERT INTO "user" (username, password_hash, role, email, department_code, created_at) VALUES
('john_smith', '...', 'teacher', 'john.smith@university.edu', 'COMP', NOW()),
```
- **Removed:** Auto-increment `id` field
- **Changed:** `department_id` → `department_code` (foreign key to department.name)
- **Note:** Email addresses updated to use university domain format

### 3. **Course Table Changes**
**Before:**
```sql
INSERT INTO course (id, name, description, department_id, teacher_id, created_at, credit, capacity, day_of_week, start_time, end_time, course_number) VALUES
(1, 'Introduction to Programming', '...', 1, 1, NOW(), 3, 30, 'Mon', '09:00:00', '11:00:00', '101'),
```

**After:**
```sql
INSERT INTO course (code, name, description, department_code, teacher_id, created_at, credit, capacity, day_of_week, start_time, end_time, course_number) VALUES
('COMP101', 'Introduction to Programming', '...', 'COMP', 1, NOW(), 3, 30, 'Mon', '09:00:00', '11:00:00', '101'),
```
- **Removed:** Auto-increment `id` field
- **Changed:** `code` is now the primary key (course code like 'COMP101')
- **Changed:** `department_id` → `department_code` (foreign key to department.name)

### 4. **Task Tables - Major Architecture Change**
**Before (Polymorphic Inheritance):**
```sql
-- Base task table with type discriminator
INSERT INTO task (id, course_id, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, type) VALUES
(1, 1, 'Python Basics Quiz', '...', 1, NOW(), ..., 'quiz');

-- Quiz-specific settings in separate table
INSERT INTO quiz (id, after_submitted_question_visible, ...) VALUES
(1, true, ...);
```

**After (Direct Models - No Inheritance):**
```sql
-- Quiz is now a complete standalone table
INSERT INTO quiz (course_code, name, description, created_by, created_at, start_datetime, end_datetime, duration, attempt_limit, point, point_in_course, after_submitted_question_visible, after_submitted_student_response_visible, after_submitted_sample_response_visible, after_submitted_class_response_visible) VALUES
('COMP101', 'Python Basics Quiz', '...', 1, NOW(), ..., true, false, true, true);
```

**Key Changes:**
- **Removed:** Base `task` table entirely
- **Changed:** Each task type is now a complete, independent table
- **Added:** All common fields (name, description, duration, etc.) directly to each task table
- **Changed:** `course_id` → `course_code` (foreign key to course.code)

### 5. **Question Table Changes**
**Before:**
```sql
INSERT INTO question (id, quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, type, content, points) VALUES
(1, 1, NULL, NULL, NULL, NULL, 'mcq', 'What is the correct way...', 2),
```

**After:**
```sql
INSERT INTO question (quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, type, content, points) VALUES
(1, NULL, NULL, NULL, NULL, 'mcq', 'What is the correct way...', 2),
```
- **Removed:** Auto-increment `id` field (handled by database)
- **Note:** Structure remains similar but now links to independent task tables

### 6. **Submission Table Changes**
**Before:**
```sql
INSERT INTO submission (id, user_id, quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, submitted_at, grade) VALUES
(1, 4, 1, NULL, NULL, NULL, NULL, NOW() - INTERVAL '2 hours', 85.5),
```

**After:**
```sql
INSERT INTO submission (user_id, quiz_id, poll_id, short_answer_id, word_cloud_id, minigame_id, submitted_at, grade) VALUES
(4, 1, NULL, NULL, NULL, NULL, NOW() - INTERVAL '2 hours', 85.5),
```
- **Removed:** Auto-increment `id` field
- **Note:** Foreign key structure remains the same

## Benefits of the Refactored Architecture

### 1. **Simplified Queries**
```sql
-- Before: Complex JOINs required
SELECT t.name, q.after_submitted_question_visible 
FROM task t 
JOIN quiz q ON t.id = q.id 
WHERE t.type = 'quiz';

-- After: Direct access
SELECT name, after_submitted_question_visible 
FROM quiz;
```

### 2. **Better Performance**
- No polymorphic identity resolution needed
- No JOINs required for basic properties
- Each table contains all necessary fields

### 3. **Clearer Schema**
- Each table represents exactly one entity type
- No type discrimination needed
- Self-documenting structure

### 4. **Easier Maintenance**
- No inheritance complexity
- Changes to one task type don't affect others
- Clear separation of concerns

## Migration Notes

### For Existing Code:
1. **Update foreign key references:**
   - `department_id` → `department_code`
   - `course_id` → `course_code`
   - Remove `task_id` references entirely

2. **Simplify queries:**
   - Remove JOINs with task table
   - Access properties directly from task-specific tables

3. **Update model relationships:**
   - Each task type now has direct relationships
   - No polymorphic identity resolution needed

### Database Schema Validation:
The refactored SQL has been tested and validated against the current model definitions in the codebase, ensuring compatibility with the Flask-SQLAlchemy models.