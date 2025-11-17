#!/usr/bin/env python
"""Check what short answer activities exist in the database"""
from app import app, db
from models import ShortAnswer

with app.app_context():
    short_answers = ShortAnswer.query.all()
    print(f"Total Short Answer activities: {len(short_answers)}")
    for sa in short_answers:
        print(f"  - ID: {sa.id}, Name: '{sa.name}', Course: {sa.course_code}, Questions: {len(sa.questions)}")
