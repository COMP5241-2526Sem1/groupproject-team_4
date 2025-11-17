#!/usr/bin/env python
"""
Check course and poll data
"""
from app import app, db
from models import Course, Poll, Question, Choice, CourseEnrollment, User

def check_data():
    with app.app_context():
        # Check courses
        courses = Course.query.all()
        print(f"\n📚 Total Courses: {len(courses)}")
        for course in courses:
            print(f"   - {course.code}: {course.name}")
        
        # Check PHYS101 specifically
        phys = Course.query.filter_by(code='PHYS101').first()
        if phys:
            print(f"\n✓ Found PHYS101: {phys.name}")
        else:
            print(f"\n❌ PHYS101 NOT FOUND")
        
        # Check poll 9
        poll = Poll.query.get(9)
        if poll:
            print(f"\n✓ Found Poll 9: {poll.name}")
            print(f"  Course: {poll.course_code}")
        else:
            print(f"\n❌ Poll 9 NOT FOUND")
        
        # Check all polls
        polls = Poll.query.all()
        print(f"\n📊 Total Polls: {len(polls)}")
        for p in polls:
            print(f"   - ID {p.id}: {p.name} (Course: {p.course_code})")
        
        # Check users
        users = User.query.all()
        print(f"\n👥 Total Users: {len(users)}")
        for user in users[:5]:
            print(f"   - {user.username} ({user.role})")
        
        # Check enrollments
        enrollments = CourseEnrollment.query.all()
        print(f"\n📝 Total Enrollments: {len(enrollments)}")

if __name__ == '__main__':
    check_data()
