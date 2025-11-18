-- SQLite compatible version of the MySQL schema
PRAGMA foreign_keys = ON;

-- 创建用户表
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username VARCHAR(50) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role TEXT CHECK(role IN ('student','teacher','admin')) NOT NULL,
  email VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建课程表
CREATE TABLE courses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  teacher_id INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  credit INTEGER DEFAULT 3 NOT NULL,
  capacity INTEGER NOT NULL,
  day_of_week VARCHAR(10),
  start_time TIME,
  end_time TIME,
  FOREIGN KEY (teacher_id) REFERENCES users(id)
);

-- 创建学生选课关系表
CREATE TABLE course_enrollments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  course_id INTEGER NOT NULL,
  student_id INTEGER NOT NULL,
  enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (course_id) REFERENCES courses(id),
  FOREIGN KEY (student_id) REFERENCES users(id)
);

-- 创建活动表
CREATE TABLE activities (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  course_id INTEGER NOT NULL,
  type TEXT CHECK(type IN ('quiz','poll','wordcloud','short_answer','game')) NOT NULL,
  title VARCHAR(100) NOT NULL,
  content TEXT, -- JSON stored as TEXT in SQLite
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- 创建提交表
CREATE TABLE submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  activity_id INTEGER NOT NULL,
  student_id INTEGER NOT NULL,
  answer TEXT, -- JSON stored as TEXT in SQLite
  score REAL,
  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (activity_id) REFERENCES activities(id),
  FOREIGN KEY (student_id) REFERENCES users(id)
);

-- 创建成绩表
CREATE TABLE grades (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  course_id INTEGER NOT NULL,
  student_id INTEGER NOT NULL,
  grade REAL,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (course_id) REFERENCES courses(id),
  FOREIGN KEY (student_id) REFERENCES users(id)
);

-- 创建通知表
CREATE TABLE notifications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sender_id INTEGER NOT NULL,
  receiver_id INTEGER NOT NULL,
  message TEXT NOT NULL,
  is_read BOOLEAN DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_id) REFERENCES users(id),
  FOREIGN KEY (receiver_id) REFERENCES users(id)
);

-- 创建系统日志表
CREATE TABLE system_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  action VARCHAR(100),
  details TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 插入测试用户(teacher)
INSERT INTO users (username, password_hash, role, email) VALUES
('seed_teacher', 'seed', 'teacher', 'teacher@example.com');

-- 插入课程数据
INSERT INTO courses (name, description, teacher_id, credit, capacity, day_of_week, start_time, end_time) VALUES
('Python Programming', 'Introduction to Python programming.', 1, 3, 50, 'Mon', '08:00:00', '11:00:00'),
('大数据分析', '数据挖掘与分析技术', 1, 3, 50, 'Fri', '16:00:00', '19:00:00');
