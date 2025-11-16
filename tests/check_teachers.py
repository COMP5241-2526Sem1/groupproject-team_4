#!/usr/bin/env python3
"""
Check what teachers are available in the database
"""

import sqlite3
import os

def check_teachers():
    """Check available teachers in the database"""
    
    try:
        # Try SQLite first (local development)
        if os.path.exists('database.db'):
            conn = sqlite3.connect('database.db')
            print("Using SQLite database")
        else:
            print("No SQLite database found")
            return False
            
        cur = conn.cursor()
        
        # Check users with teacher role
        cur.execute("SELECT id, username, password_hash, role FROM user WHERE role = 'teacher'")
        teachers = cur.fetchall()
        
        print(f"Found {len(teachers)} teachers:")
        for teacher in teachers:
            print(f"  ID: {teacher[0]}, Username: {teacher[1]}, Role: {teacher[3]}")
            print(f"  Password hash: {teacher[2][:50]}...")
        
        # Check courses and their teachers
        cur.execute("""
            SELECT c.code, c.name, u.username 
            FROM course c
            JOIN user u ON c.teacher_id = u.id
            WHERE u.role = 'teacher'
        """)
        courses = cur.fetchall()
        
        print(f"\nFound {len(courses)} courses taught by teachers:")
        for course in courses:
            print(f"  {course[0]}: {course[1]} (taught by {course[2]})")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Database error: {e}")
        return False

if __name__ == "__main__":
    print("Checking available teachers...")
    check_teachers()