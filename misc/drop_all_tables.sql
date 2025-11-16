-- SQL Script to Drop All Tables in Correct Order
-- This script drops tables in reverse dependency order to avoid foreign key violations

-- Level 7: Final grades (no dependencies)
DROP TABLE IF EXISTS grade CASCADE;

-- Level 6: Response tables
DROP TABLE IF EXISTS question_response CASCADE;
DROP TABLE IF EXISTS choice CASCADE;

-- Level 5: Content and session tables
DROP TABLE IF EXISTS word_entry CASCADE;
DROP TABLE IF EXISTS minigame_session CASCADE;
DROP TABLE IF EXISTS question CASCADE;

-- Level 4: Enrollment and submission tables
DROP TABLE IF EXISTS course_enrollment CASCADE;
DROP TABLE IF EXISTS attempt CASCADE;
DROP TABLE IF EXISTS submission CASCADE;

-- Level 3: Task inheritance tables (child tables first)
DROP TABLE IF EXISTS minigame CASCADE;
DROP TABLE IF EXISTS word_cloud CASCADE;
DROP TABLE IF EXISTS short_answer CASCADE;
DROP TABLE IF EXISTS poll CASCADE;
DROP TABLE IF EXISTS quiz CASCADE;

-- Level 2: Base task table
DROP TABLE IF EXISTS task CASCADE;

-- Level 1: Core tables (drop in reverse order)
DROP TABLE IF EXISTS course CASCADE;
DROP TABLE IF EXISTS system_log CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS department CASCADE;

-- Drop custom types if they exist
DROP TYPE IF EXISTS user_role_enum CASCADE;
DROP TYPE IF EXISTS question_type_enum CASCADE;

-- Optional: Verify all tables are dropped
-- You can run this to confirm:
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';