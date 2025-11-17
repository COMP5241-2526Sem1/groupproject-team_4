from app import app
from database import db
from models.quiz import Quiz
from models.question import Question
from models.choice import Choice

with app.app_context():
    print("=== Verifying Quiz Creation ===")
    
    # Check if quiz was created
    debug_quiz = Quiz.query.filter_by(course_code='DEBUG101').first()
    if debug_quiz:
        print(f"✅ Quiz found!")
        print(f"   ID: {debug_quiz.id}")
        print(f"   Name: {debug_quiz.name}")
        print(f"   Description: {debug_quiz.description}")
        print(f"   Course: {debug_quiz.course_code}")
        print(f"   Created by: {debug_quiz.created_by}")
        print(f"   Duration: {debug_quiz.duration} minutes")
        print(f"   Attempt limit: {debug_quiz.attempt_limit}")
        print(f"   Points: {debug_quiz.point}")
        
        # Check questions
        questions = Question.query.filter_by(quiz_id=debug_quiz.id).all()
        print(f"\n✅ Questions found: {len(questions)}")
        
        for question in questions:
            print(f"   Question ID {question.id}: {question.content}")
            print(f"   Type: {question.type}")
            print(f"   Points: {question.points}")
            
            # Check choices for MCQ
            if question.type == 'mcq':
                choices = Choice.query.filter_by(question_id=question.id).all()
                print(f"   Choices: {len(choices)}")
                for choice in choices:
                    print(f"     - {choice.content} {'(Correct)' if choice.is_correct else ''}")
            print()
    else:
        print("❌ No quiz found for DEBUG101 course")
    
    # Show all quizzes for DEBUG101
    print("=== All quizzes for DEBUG101 ===")
    all_quizzes = Quiz.query.filter_by(course_code='DEBUG101').all()
    for quiz in all_quizzes:
        print(f"Quiz: {quiz.name} (ID: {quiz.id})")