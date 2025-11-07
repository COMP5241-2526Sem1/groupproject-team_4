# Test the template logic directly
from app import app, db
from models import Quiz, User, Attempt

with app.app_context():
    # Get Quiz 6 which has submissions
    quiz = Quiz.query.get(6)
    user = User.query.filter_by(username='carol_davis').first()
    
    if quiz and user:
        print(f'Quiz 6: {quiz.name}')
        print(f'User: {user.username} (ID: {user.id})')
        
        # Get attempt count (this is what used_attempts becomes)
        attempt_count = Attempt.query.filter_by(quiz_id=6, user_id=user.id).count()
        print(f'User attempts on this quiz: {attempt_count}')
        
        print(f'Quiz visibility settings:')
        print(f'  - after_submitted_question_visible: {quiz.after_submitted_question_visible}')
        print(f'  - after_submitted_student_response_visible: {quiz.after_submitted_student_response_visible}')
        print(f'  - after_submitted_sample_response_visible: {quiz.after_submitted_sample_response_visible}')
        print(f'  - after_submitted_class_response_visible: {quiz.after_submitted_class_response_visible}')
        
        # Based on our refactor, the button should show if attempts > 0
        should_show_button = attempt_count > 0
        print(f'Should show View Response button: {should_show_button}')
        
        # The old logic would check visibility settings, but our refactor removes that
        old_logic = attempt_count > 0 and (quiz.after_submitted_question_visible or 
                                    quiz.after_submitted_student_response_visible or 
                                    quiz.after_submitted_sample_response_visible or 
                                    quiz.after_submitted_class_response_visible)
        print(f'Old logic would show button: {old_logic}')
        print(f'New logic (always show if attempts > 0): {should_show_button}')
    else:
        print('Quiz or user not found')