#!/usr/bin/env python
"""
Test the short answer detail page data
"""
from app import app, db
from models import ShortAnswer, Question, QuestionResponse

def test_short_answer_data():
    with app.app_context():
        # Get short answer ID 6
        short_answer = ShortAnswer.query.get(6)
        
        if not short_answer:
            print("❌ Short answer not found!")
            return
        
        print(f"\n📋 Short Answer: {short_answer.name}")
        print(f"   Description: {short_answer.description}")
        print(f"   ID: {short_answer.id}")
        print(f"   Questions: {len(short_answer.questions)}")
        
        # Show questions and responses
        for q_idx, question in enumerate(short_answer.questions, 1):
            print(f"\n   Q{q_idx}: {question.content}")
            print(f"   Points: {question.points}")
            print(f"   Total Responses: {len(question.question_responses)}")
            
            # Show each response
            for r_idx, response in enumerate(question.question_responses, 1):
                username = response.submission.user.username if response.submission.user else 'Unknown'
                print(f"      Response {r_idx} from {username}: {response.points}/{question.points} pts")
                print(f"         Answer: {response.text_answer[:100]}..." if len(response.text_answer or '') > 100 else f"         Answer: {response.text_answer}")

if __name__ == '__main__':
    test_short_answer_data()
