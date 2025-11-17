#!/usr/bin/env python
"""
Check poll 9 details
"""
from app import app, db
from models import Poll, Question, Choice, QuestionResponse

def check_poll():
    with app.app_context():
        # Get poll 9
        poll = Poll.query.get(9)
        
        if not poll:
            print("❌ Poll 9 not found!")
            return
        
        print(f"\n📋 Poll: {poll.name}")
        print(f"   ID: {poll.id}")
        print(f"   Description: {poll.description}")
        print(f"   Course: {poll.course_code}")
        
        # Get questions
        questions = Question.query.filter_by(poll_id=9).all()
        print(f"   Questions: {len(questions)}")
        
        for q in questions:
            print(f"\n   Q: {q.content}")
            
            # Get choices
            choices = Choice.query.filter_by(question_id=q.id).all()
            print(f"   Choices: {len(choices)}")
            
            for choice in choices:
                # Count votes
                vote_count = QuestionResponse.query.filter_by(
                    question_id=q.id,
                    choice_id=choice.id
                ).count()
                print(f"      - {choice.content}: {vote_count} votes")

if __name__ == '__main__':
    check_poll()
