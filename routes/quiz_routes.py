from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models.course import Course
from models.course_enrollment import CourseEnrollment
from models.user import User
from models.submission import Submission
from models.quiz import Quiz
from models.question import Question
from models.choice import Choice
from models.question_response import QuestionResponse
from models.attempt import Attempt
from database import db

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/course/<course_code>/quiz', methods=['GET'])
def get_quiz_list(course_code):
    # First, verify if the course exists
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    # Check if the user is enrolled in the course
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    if not enrollment:
        return render_template('course_home.html', error_message="You are not enrolled in this course",course=course), 403
    
    # Get all quizzes for the course
    quizzes = Quiz.query.filter_by(course_code=course_code).all()
    
    # Prepare data for the template
    quiz_data = []
    for quiz in quizzes:
        # Check if the user has already responded
        has_responded = Submission.query.filter_by(quiz_id=quiz.id, user_id=user_id).first() is not None
        
        # Get attempt count
        attempt_count = Attempt.query.filter_by(quiz_id=quiz.id, user_id=user_id).count()
        
        quiz_data.append({
            'id': quiz.id,
            'name': quiz.name,
            'description': quiz.description,
            'has_responded': has_responded,
            'used_attempts': attempt_count,
            'max_attempts': quiz.attempt_limit,
        })
    
    # Check for any messages (like successful submission)
    message = None
    if request.args.get('already_submitted'):
        message = "You have already responded to this quiz."
    elif request.args.get('submitted'):
        message = "Quiz submitted successfully!"
    elif not quiz_data:
        message = "No quizzes available for this course."
    
    # Render the template with the quiz data
    return render_template('quiz_list.html', course=course, quizzes=quiz_data, message=message)

@quiz_bp.route('/course/<course_code>/quiz/<int:quiz_id>', methods=['GET'])
def get_quiz_info(course_code, quiz_id):
    # Verify course exists
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    if not enrollment:
        return render_template('course_home.html', error_message="You are not enrolled in this course"), 403
    
    # Get quiz details
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_info.html', course=course, quizzes=[], error_message="Quiz not found"), 404
    
    # Get attempt count
    attempt_count = Attempt.query.filter_by(quiz_id=quiz_id, user_id=user_id).count()
    
    # Check if user can attempt again
    can_attempt = not quiz.attempt_limit or attempt_count < quiz.attempt_limit
    
    # Prepare questions with choices (for MCQ)
    quiz_data = {
        'id': quiz.id,
        'name': quiz.name,
        'description': quiz.description,
        'used_attempts': attempt_count,
        'max_attempts': quiz.attempt_limit,
        'can_attempt': can_attempt,
        'questions': []
    }

    return render_template('quiz_info.html', course=course, quiz=quiz_data, course_code=course_code)

@quiz_bp.route('/course/<course_code>/quiz/<int:quiz_id>/start', methods=['GET'])
def start_quiz(course_code, quiz_id):
    # Verify course exists
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    if not enrollment:
        return render_template('course_home.html', error_message="You are not enrolled in this course"), 403
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_list.html', course=course, quizzes=[], error_message="Quiz not found"), 404
    
    # Check if user has already submitted
    has_responded = Submission.query.filter_by(quiz_id=quiz_id, user_id=user_id).first() is not None
    
    # Get attempt count
    attempt_count = Attempt.query.filter_by(quiz_id=quiz_id, user_id=user_id).count()
    
    # Check if user can attempt again
    if quiz.attempt_limit and attempt_count >= quiz.attempt_limit:
        return render_template('quiz_info.html', course=course, quiz={
            'id': quiz.id,
            'name': quiz.name,
            'description': quiz.description,
            'has_responded': has_responded,
            'used_attempts': attempt_count,
            'max_attempts': quiz.attempt_limit,
            'can_attempt': False
        }, error_message="You have reached the maximum number of attempts for this quiz"), 400
    
    # Get quiz questions
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Create new attempt
    new_attempt = Attempt(quiz_id=quiz_id, user_id=user_id, attempt_count=attempt_count + 1)
    db.session.add(new_attempt)
    db.session.commit()
    
    # Store attempt ID in session for later use
    session['current_attempt_id'] = new_attempt.id
    
    # Prepare questions with choices
    quiz_data = {
        'id': quiz.id,
        'name': quiz.name,
        'description': quiz.description,
        'duration': quiz.duration,
        'has_responded': has_responded,
        'used_attempts': attempt_count,
        'max_attempts': quiz.attempt_limit,
        'can_attempt': True,
        'deadline': getattr(quiz, 'deadline', None),
        'questions': [{
            'id': q.id,
            'content': q.content,
            'type': q.type,
            'points': q.points,
            'choices': [{'id': c.id, 'content': c.content} for c in q.choices] if q.type == 'mcq' else []
        } for q in questions]
    }
    
    return render_template('quiz_start.html', course=course, quiz=quiz_data, course_code=course_code)

@quiz_bp.route('/course/<course_code>/quiz/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(course_code, quiz_id):
    # Verify course exists
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    if not enrollment:
        return render_template('course_home.html', error_message="You are not enrolled in this course"), 403
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_list.html', course=course, quizzes=[], error_message="Quiz not found"), 404
    
    # Get current attempt ID from session
    attempt_id = session.get('current_attempt_id')
    if not attempt_id:
        return render_template('quiz_start.html', course=course, quiz=quiz, error_message="No active quiz attempt found"), 400
    
    # Get the attempt
    attempt = Attempt.query.filter_by(id=attempt_id, user_id=user_id, quiz_id=quiz_id).first()
    if not attempt:
        return render_template('quiz_start.html', course=course, quiz=quiz, error_message="Invalid quiz attempt"), 400
    
    # Get all questions for this quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Process answers first to calculate scores
    total_points = 0
    all_answers_correct = True
    
    for question in questions:
        answer_key = f"question-{question.id}"
        user_answer = request.form.get(answer_key)
        
        if question.type == 'mcq':
            # Check if answer is provided
            if not user_answer:
                all_answers_correct = False
                # Create response with empty answer
                response = QuestionResponse(
                    submission_id=submission.id,
                    question_id=question.id,
                    choice_id=None,
                    text_answer=None,
                    is_correct=False
                )
                db.session.add(response)
            else:
                # Get the choice
                choice = Choice.query.get(user_answer)
                if choice:
                    # Check if correct
                    is_correct = choice.is_correct
                    if not is_correct:
                        all_answers_correct = False
                    
                    # Award points if correct
                    points_awarded = question.points if is_correct else 0
                    total_points += points_awarded
                    
                    # Create response
                    response = QuestionResponse(
                        submission_id=submission.id,
                        question_id=question.id,
                        choice_id=choice.id,
                        text_answer=None,
                        is_correct=is_correct
                    )
                    db.session.add(response)
        elif question.type == 'saq':
            # For short answer questions, just store the text
            # Note: In a real system, you might want to implement answer checking logic
            points_awarded = 0  # Default to 0 for manual grading
            
            # Create response
            response = QuestionResponse(
                submission_id=submission.id,
                question_id=question.id,
                choice_id=None,
                text_answer=user_answer,
                is_correct=False  # Mark as incorrect until manually graded
            )
            db.session.add(response)
    
    # Create submission record after processing answers
    submission = Submission(
        user_id=user_id,
        quiz_id=quiz_id,
        attempt_id=attempt_id,
        score=total_points,
        is_passed=all_answers_correct  # This is a simple pass/fail logic
    )
    db.session.add(submission)
    
    # Update attempt with score
    attempt.score = total_points
    attempt.is_completed = True
    
    # Save all changes
    db.session.commit()
    
    # Clear the current attempt from session
    if 'current_attempt_id' in session:
        del session['current_attempt_id']
    
    # Redirect to quiz list with success message
    return redirect(f'/course/{course_code}/quiz?submitted=1')