# Direct Quiz Model - No Task Inheritance

## Overview

The educational management system now uses **direct models** instead of polymorphic inheritance. Each task type (Quiz, Poll, ShortAnswer, WordCloud, Minigame) is a completely independent table with its own properties.

## Key Changes

1. **No Task Table**: The `task` table has been removed
2. **Direct Properties**: Each model has its own `name`, `description`, `duration`, `point`, etc.
3. **Independent Tables**: Each task type has its own table with all required fields
4. **No Type Discriminator**: No need for `type` column since each table represents one specific task type

## Database Schema

```sql
-- Quiz table (standalone, no inheritance)
CREATE TABLE quiz (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,           -- Direct property
    description TEXT,                       -- Direct property
    course_id INTEGER REFERENCES course(id),
    created_by INTEGER REFERENCES "user"(id),
    duration INTEGER DEFAULT 30,
    point INTEGER DEFAULT 100,
    after_submitted_question_visible BOOLEAN DEFAULT FALSE,
    after_submitted_student_response_visible BOOLEAN DEFAULT FALSE,
    after_submitted_sample_response_visible BOOLEAN DEFAULT FALSE,
    after_submitted_class_response_visible BOOLEAN DEFAULT FALSE
);

-- Poll table (standalone, no inheritance)
CREATE TABLE poll (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    course_id INTEGER REFERENCES course(id),
    created_by INTEGER REFERENCES "user"(id),
    duration INTEGER DEFAULT 30,
    point INTEGER DEFAULT 0
);

-- Similar structure for short_answer, word_cloud, minigame tables
```

## How to Query Quiz with its Name

Since Quiz is now a standalone table, you can access properties directly:

### Method 1: Simple SQL Query
```sql
SELECT 
    q.id AS quiz_id,
    q.name AS quiz_name,                    -- ✅ Direct access to name
    q.description AS quiz_description,
    q.duration,
    q.point,
    q.after_submitted_question_visible,
    q.after_submitted_student_response_visible
FROM quiz q
LIMIT 5;
```

### Method 2: Direct Access (In SQLAlchemy/Python)
```python
quiz = db.session.query(Quiz).first()
print(quiz.name)  # ✅ Direct access to name property
```

### Method 3: Query with Course Information
```sql
SELECT 
    q.id,
    q.name AS quiz_name,                    -- ✅ Direct from quiz table
    c.code AS course_code,
    c.name AS course_name,
    q.start_datetime,
    q.end_datetime,
    q.attempt_limit,
    q.after_submitted_question_visible
FROM quiz q
JOIN course c ON q.course_id = c.id
ORDER BY q.name;
```

## Key Benefits

1. **Simpler Queries**: No JOINs needed to get basic properties
2. **Better Performance**: No polymorphic identity resolution
3. **Clearer Schema**: Each table represents exactly one entity type
4. **Easier Maintenance**: No inheritance complexity

## Practical Examples

### Get all quizzes with names:
```sql
SELECT q.id, q.name AS quiz_name, q.description
FROM quiz q
ORDER BY q.name;
```

### Get quiz submissions with quiz names:
```sql
SELECT 
    s.id AS submission_id,
    u.username,
    q.name AS quiz_name,                    -- ✅ Direct from quiz table
    s.grade,
    s.submitted_at
FROM submission s
JOIN quiz q ON s.quiz_id = q.id
JOIN "user" u ON s.user_id = u.id
ORDER BY s.submitted_at DESC;
```

### Count questions per quiz:
```sql
SELECT 
    q.id,
    q.name AS quiz_name,                    -- ✅ Direct from quiz table
    COUNT(quest.id) AS question_count
FROM quiz q
LEFT JOIN question quest ON q.id = quest.quiz_id
GROUP BY q.id, q.name;
```

## Migration Notes

If you're migrating from the old polymorphic system:

1. **Update Queries**: Remove JOINs with task table
2. **Direct Access**: Use table properties directly
3. **No Type Checks**: No need to filter by `type` column
4. **Schema Updates**: Each model now has all required fields

## Summary

**Answer to your question**: Yes! When you select from `quiz`, you can get its `name` directly from the quiz table itself. No JOINs or inheritance complexity needed - the `name` property is now a direct column in the `quiz` table.