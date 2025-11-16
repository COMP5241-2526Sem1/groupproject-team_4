from app import app
from models.poll import Poll
from models.quiz import Quiz
from datetime import datetime

with app.app_context():
    print('=== POLLS ===')
    polls = Poll.query.all()
    for p in polls:
        print(f'ID: {p.id}, Name: {p.name}')
        print(f'  Start: {p.start_datetime}')
        print(f'  End: {p.end_datetime}')
        print(f'  Course: {p.course_code}')
        print()
    
    print('=== QUIZZES ===')
    quizzes = Quiz.query.all()
    for q in quizzes:
        print(f'ID: {q.id}, Name: {q.name}')
        print(f'  Start: {q.start_datetime}')
        print(f'  End: {q.end_datetime}')
        print(f'  Course: {q.course_code}')
        print()
    
    print(f'Current time: {datetime.now()}')