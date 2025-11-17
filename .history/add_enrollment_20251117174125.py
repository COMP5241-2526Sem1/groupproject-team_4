#!/usr/bin/env python
"""
Add current user to PHYS101 course
"""
from app import app, db
from models import User, CourseEnrollment

def add_enrollment():
    with app.app_context():
        # Get the teacher user (john_smith based on the login screen)
        user = User.query.filter_by(username='john_smith').first()
        if not user:
            print("❌ john_smith not found")
            return
        
        print(f"✓ Found user: {user.username} (ID: {user.id})")
        
        # Check if already enrolled
        enrolled = CourseEnrollment.query.filter_by(
            student_id=user.id,
            course_code='PHYS101'
        ).first()
        
        if enrolled:
            print(f"✓ Already enrolled in PHYS101")
        else:
            print(f"Adding enrollment...")
            enrollment = CourseEnrollment(
                student_id=user.id,
                course_code='PHYS101'
            )
            db.session.add(enrollment)
            db.session.commit()
            print(f"✓ Added enrollment to PHYS101")
        
        # Also add other users
        for username in ['alice_johnson', 'bob_williams', 'carol_davis']:
            user = User.query.filter_by(username=username).first()
            if user:
                enrolled = CourseEnrollment.query.filter_by(
                    student_id=user.id,
                    course_code='PHYS101'
                ).first()
                
                if not enrolled:
                    enrollment = CourseEnrollment(
                        student_id=user.id,
                        course_code='PHYS101'
                    )
                    db.session.add(enrollment)
                    db.session.commit()
                    print(f"✓ Added {username} to PHYS101")
                else:
                    print(f"✓ {username} already enrolled")

if __name__ == '__main__':
    add_enrollment()
