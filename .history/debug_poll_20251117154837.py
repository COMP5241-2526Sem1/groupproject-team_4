from app import app
from models.poll import Poll
from models.question import Question
from models.choice import Choice

with app.app_context():
    poll = Poll.query.filter_by(id=5).first()
    print(f"Poll ID=5: {poll}")
    
    if poll:
        print(f"Poll name: {poll.name}")
        print(f"Poll course: {poll.course_code}")
        
        questions = Question.query.filter_by(poll_id=5).all()
        print(f"Total questions: {len(questions)}")
        
        for q in questions:
            print(f"\n  Question ID={q.id}: {q.content}")
            choices = Choice.query.filter_by(question_id=q.id).all()
            print(f"  Choices: {len(choices)}")
            for c in choices:
                print(f"    - {c.content}")
    else:
        print("Poll not found!")
