#!/usr/bin/env python3
"""Check who is enrolled in PHYS101 course"""

from app import app, db
from models.course_enrollment import CourseEnrollment
from models.user import User
from models.course import Course

with app.app_context():
    # Find PHYS101 course
    phys_course = Course.query.filter_by(code='PHYS101').first()
    if not phys_course:
        print("PHYS101 course not found!")
        exit(1)
    
    print(f"PHYS101 Course Code: {phys_course.code}")
    print(f"Course Name: {phys_course.name}")
    print(f"Teacher ID: {phys_course.teacher_id}")
    
    # Find teacher
    teacher = User.query.get(phys_course.teacher_id)
    if teacher:
        print(f"Teacher: {teacher.username} ({teacher.email})")
    
    # Find all enrollments for PHYS101
    enrollments = CourseEnrollment.query.filter_by(course_code=phys_course.code).all()
    print(f"\nTotal enrollments: {len(enrollments)}")
    
    for enrollment in enrollments:
        user = User.query.get(enrollment.student_id)
        if user:
            print(f"Student: {user.username} ({user.email}) - Role: {user.role}")