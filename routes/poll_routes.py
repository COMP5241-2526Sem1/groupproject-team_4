from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models.course import Course
from models.course_enrollment import CourseEnrollment
from models.user import User
from models.poll import Poll
from models.question import Question
from models.choice import Choice
from models.question_response import QuestionResponse
from database import db

poll_bp = Blueprint('poll', __name__)

@poll_bp.route('/course/<course_id>/poll', methods=['GET'])
def get_poll_list(course_id):
    # First, verify if the course exists
    course = Course.query.get(course_id)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    # Check if the user is enrolled in the course
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_id=course_id).first()
    if not enrollment:
        return render_template('course_home.html', error_message="You are not enrolled in this course"), 403
    
    # Get all polls for the course
    polls = Poll.query.filter_by(course_id=course_id).all()
    
    # Prepare data for the template
    poll_data = []
    for poll in polls:
        # Check if the user has already responded
        has_responded = QuestionResponse.query.join(Question).filter(
            Question.poll_id == poll.id,
            QuestionResponse.student_id == user_id
        ).first() is not None
        
        poll_data.append({
            'id': poll.id,
            'title': poll.title,
            'description': poll.description,
            'has_responded': has_responded,
            'deadline': poll.deadline
        })
    
    # Check for any messages (like successful submission)
    message = None
    if request.args.get('already_submitted'):
        message = "You have already responded to this poll."
    elif request.args.get('submitted'):
        message = "Poll submitted successfully!"
    elif not poll_data:
        message = "No polls available for this course."
    
    # Render the template with the poll data
    return render_template('poll_list.html', course=course, polls=poll_data, message=message)

@poll_bp.route('/course/<course_id>/poll/<int:poll_id>', methods=['GET'])
def get_poll_info(course_id, poll_id):
    # Verify course exists
    course = Course.query.get(course_id)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_id=course_id).first()
    if not enrollment:
        return render_template('course_home.html', error_message="You are not enrolled in this course"), 403
    
    # Get poll details
    poll = Poll.query.filter_by(id=poll_id, course_id=course_id).first()
    if not poll:
        return render_template('poll_list.html', course=course, polls=[], error_message="Poll not found"), 404
    
    # Get poll questions
    questions = Question.query.filter_by(poll_id=poll_id).all()
    
    # Check if user has already responded
    has_responded = QuestionResponse.query.join(Question).filter(
        Question.poll_id == poll_id,
        QuestionResponse.student_id == user_id
    ).first() is not None
    
    # Prepare questions with choices (for MCQ)
    poll_data = {
        'id': poll.id,
        'title': poll.title,
        'description': poll.description,
        'has_responded': has_responded,
        'deadline': poll.deadline,
        'questions': []
    }
    
    for question in questions:
        q_data = {
            'id': question.id,
            'content': question.content,
            'type': question.type
        }
        
        if question.type == 'mcq':
            choices = Choice.query.filter_by(question_id=question.id).all()
            q_data['choices'] = [{'id': c.id, 'content': c.content} for c in choices]
        
        poll_data['questions'].append(q_data)
    
    return render_template('poll_info.html', course=course, poll=poll_data)

@poll_bp.route('/course/<course_id>/poll/<int:poll_id>/start', methods=['GET'])
def start_poll(course_id, poll_id):
    # Verify course exists
    course = Course.query.get(course_id)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_id=course_id).first()
    if not enrollment:
        return render_template('course_home.html', error_message="You are not enrolled in this course"), 403
    
    # Get poll
    poll = Poll.query.filter_by(id=poll_id, course_id=course_id).first()
    if not poll:
        return render_template('poll_list.html', course=course, polls=[], error_message="Poll not found"), 404
    
    # Check if user has already responded
    has_responded = QuestionResponse.query.join(Question).filter(
        Question.poll_id == poll_id,
        QuestionResponse.student_id == user_id
    ).first() is not None
    
    if has_responded:
        return redirect(f'/course/{course_id}/poll?already_submitted=1')
    
    # Get poll questions
    questions = Question.query.filter_by(poll_id=poll_id).all()
    
    # Prepare questions with choices
    poll_data = {
        'id': poll.id,
        'title': poll.title,
        'description': poll.description
    }
    
    question_list = []
    for question in questions:
        q_data = {
            'id': question.id,
            'content': question.content,
            'type': question.type
        }
        
        if question.type == 'mcq':
            choices = Choice.query.filter_by(question_id=question.id).all()
            q_data['choices'] = [{'id': c.id, 'content': c.content} for c in choices]
        
        question_list.append(q_data)
    
    return render_template('poll_start.html', course=course, poll=poll_data, questions=question_list, course_id=course_id)

@poll_bp.route('/course/<course_id>/poll/<int:poll_id>/submit', methods=['POST'])
def submit_poll(course_id, poll_id):
    # Verify course exists
    course = Course.query.get(course_id)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_id=course_id).first()
    if not enrollment:
        return render_template('course_home.html', error_message="You are not enrolled in this course"), 403
    
    # Get poll
    poll = Poll.query.filter_by(id=poll_id, course_id=course_id).first()
    if not poll:
        return render_template('poll_list.html', course=course, polls=[], error_message="Poll not found"), 404
    
    # Check if user has already responded
    has_responded = QuestionResponse.query.join(Question).filter(
        Question.poll_id == poll_id,
        QuestionResponse.student_id == user_id
    ).first() is not None
    
    if has_responded:
        return redirect(f'/course/{course_id}/poll?already_submitted=1')
    
    # Get all questions for this poll
    questions = Question.query.filter_by(poll_id=poll_id).all()
    
    # Process answers
    for question in questions:
        answer_key = f"question-{question.id}"
        user_answer = request.form.get(answer_key)
        
        if question.type == 'mcq':
            # Create response for MCQ
            response = QuestionResponse(
                student_id=user_id,
                question_id=question.id,
                choice_id=user_answer,  # This could be None if no answer provided
                text_answer=None
            )
            db.session.add(response)
        elif question.type == 'saq':
            # Create response for short answer question
            response = QuestionResponse(
                student_id=user_id,
                question_id=question.id,
                choice_id=None,
                text_answer=user_answer  # This could be None if no answer provided
            )
            db.session.add(response)
    
    # Save all changes
    db.session.commit()
    
    # Redirect to poll list with success message
    return redirect(f'/course/{course_id}/poll?submitted=1')