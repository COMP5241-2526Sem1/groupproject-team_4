#!/usr/bin/env python
"""List all short answer activities in PHYS101"""
from app import app, db
from models import ShortAnswer

with app.app_context():
    sas = ShortAnswer.query.filter_by(course_code='PHYS101').all()
    print(f"Short Answer activities in PHYS101:\n")
    
    for sa in sas:
        print(f"ID: {sa.id}")
        print(f"Name: '{sa.name}'")
        print(f"Description: {sa.description}")
        print(f"Questions: {len(sa.questions)}")
        print(f"Submissions: {len(sa.submissions)}")
        print("-" * 60)
