from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from models.course import Course
from models.course_enrollment import CourseEnrollment
from models.user import User
from models.poll import Poll
from models.question import Question
from models.choice import Choice
from models.question_response import QuestionResponse
from models.submission import Submission
from database import db
from datetime import datetime

poll_bp = Blueprint('poll', __name__)

@poll_bp.route('/course/<course_code>/poll', methods=['GET'])
def get_poll_list(course_code):
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
        return render_template('course_home.html', error_message="You are not enrolled in this course"), 403
    
    # Get all polls for the course
    polls = Poll.query.filter_by(course_code=course_code).all()
    
    # Check if user is teacher (teachers have unlimited attempts)
    user = User.query.get(user_id)
    is_teacher = user and user.role == 'teacher'
    
    # Prepare data for the template
    poll_data = []
    for poll in polls:
        # Get submission count (similar to attempt count for quizzes)
        submission_count = Submission.query.filter_by(poll_id=poll.id, user_id=user_id).count()
        
        # Check if user can attempt again (teachers always can)
        can_attempt = is_teacher or not poll.attempt_limit or submission_count < poll.attempt_limit
        
        # Check if poll is currently available (within start and end datetime)
        current_time = datetime.now()
        is_available = True
        if poll.start_datetime and current_time < poll.start_datetime:
            is_available = False
        if poll.end_datetime and current_time > poll.end_datetime:
            is_available = False
        
        poll_data.append({
            'id': poll.id,
            'name': poll.name,
            'description': poll.description,
            'used_attempts': submission_count,
            'max_attempts': poll.attempt_limit if poll.attempt_limit else 0,
            'can_attempt': can_attempt,
            'start_datetime': poll.start_datetime,
            'end_datetime': poll.end_datetime,
            'is_available': is_available
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

@poll_bp.route('/course/<course_code>/poll/<int:poll_id>', methods=['GET'])
def get_poll_info(course_code, poll_id):
    # Verify course exists
    course = Course.query.filter_by(code=course_code).first()
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
    
    # Get poll details
    poll = Poll.query.filter_by(id=poll_id, course_code=course_code).first()
    if not poll:
        return render_template('poll_list.html', course=course, polls=[], error_message="Poll not found"), 404
    
    # Get submission count (similar to attempt count for quizzes)
    submission_count = Submission.query.filter_by(poll_id=poll_id, user_id=user_id).count()
    
    # Check if user is teacher (teachers have unlimited attempts)
    user = User.query.get(user_id)
    is_teacher = user and user.role == 'teacher'
    
    # Check if user can attempt again (teachers always can)
    can_attempt = is_teacher or not poll.attempt_limit or submission_count < poll.attempt_limit
    
    # If student has used all attempts and cannot view results (no submissions), redirect to poll list
    # Students can only view results if they have at least one submission
    if not is_teacher and not can_attempt and submission_count == 0:
        return redirect(f'/course/{course_code}/poll')
    
    # Get poll questions
    questions = Question.query.filter_by(poll_id=poll_id).all()
    
    # Prepare questions with choices (for MCQ)
    poll_data = {
        'id': poll.id,
        'name': poll.name,
        'description': poll.description,
        'used_attempts': submission_count,
        'max_attempts': poll.attempt_limit if poll.attempt_limit else 0,
        'can_attempt': can_attempt,
        'start_datetime': poll.start_datetime,
        'end_datetime': poll.end_datetime,
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
            choices_data = []
            for choice in choices:
                # Count how many submissions chose this choice
                vote_count = QuestionResponse.query.filter_by(
                    question_id=question.id,
                    choice_id=choice.id
                ).count()
                choices_data.append({
                    'id': choice.id,
                    'content': choice.content,
                    'vote_count': vote_count
                })
            q_data['choices'] = choices_data
        
        poll_data['questions'].append(q_data)
    
    return render_template('poll_info.html', course=course, poll=poll_data)

@poll_bp.route('/course/<course_code>/poll/<int:poll_id>/start', methods=['GET'])
def start_poll(course_code, poll_id):
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
    
    # Get poll
    poll = Poll.query.filter_by(id=poll_id, course_code=course_code).first()
    if not poll:
        return render_template('poll_list.html', course=course, polls=[], error_message="Poll not found"), 404
    
    # Get submission count (similar to attempt count for quizzes)
    submission_count = Submission.query.filter_by(poll_id=poll_id, user_id=user_id).count()
    
    # Check if user is teacher (teachers have unlimited attempts)
    user = User.query.get(user_id)
    is_teacher = user and user.role == 'teacher'
    
    # Check if user can attempt again (teachers always can)
    can_attempt = is_teacher or not poll.attempt_limit or submission_count < poll.attempt_limit
    
    # Check if poll is currently available (within start and end datetime)
    current_time = datetime.now()
    is_available = True
    if poll.start_datetime and current_time < poll.start_datetime:
        is_available = False
    if poll.end_datetime and current_time > poll.end_datetime:
        is_available = False
    
    if not is_available:
        return render_template('poll_info.html', course=course, poll={
            'id': poll.id,
            'name': poll.name,
            'description': poll.description,
            'used_attempts': submission_count,
            'max_attempts': poll.attempt_limit if poll.attempt_limit else 0,
            'can_attempt': False,
            'start_datetime': poll.start_datetime,
            'end_datetime': poll.end_datetime
        }, error_message="This poll is not currently available"), 400
    
    if not can_attempt:
        return redirect(f'/course/{course_code}/poll?already_submitted=1')
    
    # Get poll questions
    questions = Question.query.filter_by(poll_id=poll_id).all()
    
    # Prepare questions with choices
    poll_data = {
        'id': poll.id,
        'name': poll.name,
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
    
    return render_template('poll_start.html', course=course, poll=poll_data, questions=question_list, course_code=course_code)

@poll_bp.route('/course/<course_code>/poll/<int:poll_id>/results', methods=['GET'])
def get_poll_results(course_code, poll_id):
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
    
    # Get poll
    poll = Poll.query.filter_by(id=poll_id, course_code=course_code).first()
    if not poll:
        return render_template('poll_list.html', course=course, polls=[], error_message="Poll not found"), 404
    
    # Get submission count to validate access
    submission_count = Submission.query.filter_by(poll_id=poll_id, user_id=user_id).count()
    
    # Check if user is teacher (teachers can always view results)
    user = User.query.get(user_id)
    is_teacher = user and user.role == 'teacher'
    
    # Students can only view results if they have at least one submission
    if not is_teacher and submission_count == 0:
        return redirect(f'/course/{course_code}/poll')
    
    # Get user's submission
    submission = Submission.query.filter_by(poll_id=poll_id, user_id=user_id).first()
    if not submission:
        return render_template('poll_results.html', course=course, poll=poll, error_message="No submission found for this poll"), 404
    
    # Get all question responses for this submission
    responses = QuestionResponse.query.filter_by(submission_id=submission.id).all()
    
    # Prepare results data based on poll visibility settings (always visible for polls)
    results_data = {
        'id': poll.id,
        'name': poll.name,
        'description': poll.description,
        'submitted_at': submission.submitted_at,
        'visibility': {
            'question_visible': True,  # Polls always show questions
            'student_response_visible': True,  # Polls always show responses
            'sample_response_visible': True,  # Polls always show sample responses
            'class_response_visible': True   # Polls always show class responses
        },
        'questions': []
    }
    
    for response in responses:
        question = Question.query.get(response.question_id)
        if not question:
            continue
            
        question_data = {
            'id': question.id,
            'content': question.content,
            'type': question.type,
            'user_answer': None,
            'correct_answer': None,
            'class_responses': []
        }
        
        # Show question content (always visible for polls)
        question_data['content'] = question.content
        
        # Show student response (always visible for polls)
        if question.type == 'mcq':
            if response.choice_id:
                choice = Choice.query.get(response.choice_id)
                if choice:
                    question_data['user_answer'] = choice.content
        elif question.type == 'saq':
            question_data['user_answer'] = response.text_answer
        
        # Show class responses (always visible for polls)
        if question.type == 'mcq':
            # Get all responses for this question across all submissions
            all_responses = QuestionResponse.query.join(Submission).filter(
                QuestionResponse.question_id == question.id,
                Submission.poll_id == poll_id
            ).all()
            
            # Count responses for each choice
            choice_counts = {}
            total_responses = len(all_responses)
            
            for resp in all_responses:
                if resp.choice_id:
                    choice = Choice.query.get(resp.choice_id)
                    if choice:
                        if choice.content not in choice_counts:
                            choice_counts[choice.content] = 0
                        choice_counts[choice.content] += 1
            
            # Calculate percentages
            for choice_text, count in choice_counts.items():
                percentage = (count / total_responses * 100) if total_responses > 0 else 0
                question_data['class_responses'].append({
                    'choice': choice_text,
                    'count': count,
                    'percentage': round(percentage, 1)
                })
        
        results_data['questions'].append(question_data)
    
    # Get class statistics (always visible for polls)
    all_submissions = Submission.query.filter_by(poll_id=poll_id).all()
    total_students = len(all_submissions)
    results_data['class_statistics'] = {
        'total_students': total_students
    }
    
    return render_template('poll_results.html', course=course, poll=results_data, course_code=course_code)


@poll_bp.route('/api/poll/<int:poll_id>/results', methods=['GET'])
def get_poll_results_data(poll_id):
    """API endpoint for poll results data with HTTP caching"""
    # Get course code from request args
    course_code = request.args.get('course_code')
    if not course_code:
        return jsonify({'error': 'course_code parameter is required'}), 400
    
    # Verify course exists
    course = Course.query.get(course_code)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    if not enrollment:
        return jsonify({'error': 'You are not enrolled in this course'}), 403
    
    # Get poll
    poll = Poll.query.filter_by(id=poll_id, course_code=course_code).first()
    if not poll:
        return jsonify({'error': 'Poll not found'}), 404
    
    # Get submission count to validate access
    submission_count = Submission.query.filter_by(poll_id=poll_id, user_id=user_id).count()
    
    # Check if user is teacher (teachers can always view results)
    user = User.query.get(user_id)
    is_teacher = user and user.role == 'teacher'
    
    # Students can only view results if they have at least one submission
    if not is_teacher and submission_count == 0:
        return jsonify({'error': 'No submission found for this poll'}), 403
    
    # Get user's submission
    submission = Submission.query.filter_by(poll_id=poll_id, user_id=user_id).first()
    if not submission:
        return jsonify({'error': 'No submission found for this poll'}), 404
    
    # Get all question responses for this submission
    responses = QuestionResponse.query.filter_by(submission_id=submission.id).all()
    
    # Prepare results data based on poll visibility settings (always visible for polls)
    results_data = {
        'id': poll.id,
        'name': poll.name,
        'description': poll.description,
        'submitted_at': submission.submitted_at.isoformat() if submission.submitted_at else None,
        'visibility': {
            'question_visible': True,  # Polls always show questions
            'student_response_visible': True,  # Polls always show responses
            'sample_response_visible': True,  # Polls always show sample responses
            'class_response_visible': True   # Polls always show class responses
        },
        'questions': [],
        'class_statistics': {}
    }
    
    for response in responses:
        question = Question.query.get(response.question_id)
        if not question:
            continue
            
        question_data = {
            'id': question.id,
            'content': question.content,
            'type': question.type,
            'user_answer': None,
            'correct_answer': None,
            'class_responses': []
        }
        
        # Show question content (always visible for polls)
        question_data['content'] = question.content
        
        # Show student response (always visible for polls)
        if question.type == 'mcq':
            if response.choice_id:
                choice = Choice.query.get(response.choice_id)
                if choice:
                    question_data['user_answer'] = choice.content
        elif question.type == 'saq':
            question_data['user_answer'] = response.text_answer
        
        # Show class responses (always visible for polls)
        if question.type == 'mcq':
            # Get all responses for this question across all submissions
            all_responses = QuestionResponse.query.join(Submission).filter(
                QuestionResponse.question_id == question.id,
                Submission.poll_id == poll_id
            ).all()
            
            # Count responses for each choice
            choice_counts = {}
            total_responses = len(all_responses)
            
            for resp in all_responses:
                if resp.choice_id:
                    choice = Choice.query.get(resp.choice_id)
                    if choice:
                        if choice.content not in choice_counts:
                            choice_counts[choice.content] = 0
                        choice_counts[choice.content] += 1
            
            # Calculate percentages
            for choice_text, count in choice_counts.items():
                percentage = (count / total_responses * 100) if total_responses > 0 else 0
                question_data['class_responses'].append({
                    'choice': choice_text,
                    'count': count,
                    'percentage': round(percentage, 1)
                })
        
        results_data['questions'].append(question_data)
    
    # Get class statistics (always visible for polls)
    all_submissions = Submission.query.filter_by(poll_id=poll_id).all()
    total_students = len(all_submissions)
    results_data['class_statistics'] = {
        'total_students': total_students
    }
    
    # Generate ETag based on data content
    import hashlib
    import json
    data_str = json.dumps(results_data, sort_keys=True)
    etag = hashlib.md5(data_str.encode()).hexdigest()
    
    # Check if client has cached version
    if_none_match = request.headers.get('If-None-Match')
    if if_none_match and if_none_match == etag:
        app.logger.info(f"Poll results data cache hit for poll {poll_id}")
        return '', 304
    
    app.logger.info(f"Poll results data cache miss for poll {poll_id}")
    
    # Return data with caching headers
    response = jsonify(results_data)
    response.headers['ETag'] = etag
    response.headers['Cache-Control'] = 'private, must-revalidate'
    return response, 200


# Teacher poll management routes
@poll_bp.route('/teacher/course/<course_code>/poll', methods=['GET'])
def teacher_poll_list(course_code):
    # Check if user is logged in and is a teacher
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if not user or user.role != 'teacher':
        return render_template('course_home.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    if course.teacher_id != user_id:
        return render_template('course_home.html', error_message="You are not the teacher of this course"), 403
    
    # Get all polls for the course
    polls = Poll.query.filter_by(course_code=course_code).all()
    
    return render_template('teacher_poll_list.html', course=course, polls=polls)

@poll_bp.route('/teacher/course/<course_code>/poll/create', methods=['GET', 'POST'])
def teacher_create_poll(course_code):
    # Check if user is logged in and is a teacher
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if not user or user.role != 'teacher':
        return render_template('course_home.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    if course.teacher_id != user_id:
        return render_template('course_home.html', error_message="You are not the teacher of this course"), 403
    
    if request.method == 'POST':
        # Create new poll (always visible for polls)
        poll = Poll(
            course_code=course_code,
            name=request.form['name'],
            description=request.form['description'],
            created_by=user_id,
            duration=int(request.form.get('duration', 30)),
            attempt_limit=int(request.form.get('attempt_limit', 5)),
            point=0,  # Polls are ungraded
            point_in_course=0,
            # Polls should always be visible
            after_submitted_question_visible=True,
            after_submitted_student_response_visible=True,
            after_submitted_sample_response_visible=True,
            after_submitted_class_response_visible=True
        )
        
        db.session.add(poll)
        db.session.commit()
        
        flash('Poll created successfully!')
        return redirect(url_for('poll.teacher_poll_list', course_code=course_code))
    
    return render_template('teacher_create_poll.html', course=course)

@poll_bp.route('/teacher/course/<course_code>/poll/<int:poll_id>/edit', methods=['GET', 'POST'])
def teacher_edit_poll(course_code, poll_id):
    # Check if user is logged in and is a teacher
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if not user or user.role != 'teacher':
        return render_template('course_home.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    if course.teacher_id != user_id:
        return render_template('course_home.html', error_message="You are not the teacher of this course"), 403
    
    # Get poll
    poll = Poll.query.filter_by(id=poll_id, course_code=course_code).first()
    if not poll:
        return render_template('course_home.html', error_message="Poll not found"), 404
    
    if request.method == 'POST':
        # Update poll
        poll.name = request.form['name']
        poll.description = request.form['description']
        poll.duration = int(request.form.get('duration', 30))
        poll.attempt_limit = int(request.form.get('attempt_limit', 5))
        # Polls remain ungraded and always visible
        poll.point = 0
        poll.point_in_course = 0
        poll.after_submitted_question_visible = True
        poll.after_submitted_student_response_visible = True
        poll.after_submitted_sample_response_visible = True
        poll.after_submitted_class_response_visible = True
        
        db.session.commit()
        
        flash('Poll updated successfully!')
        return redirect(url_for('poll.teacher_poll_list', course_code=course_code))
    
    return render_template('teacher_edit_poll.html', course=course, poll=poll)

@poll_bp.route('/teacher/course/<course_code>/poll/<int:poll_id>/delete', methods=['POST'])
def teacher_delete_poll(course_code, poll_id):
    # Check if user is logged in and is a teacher
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if not user or user.role != 'teacher':
        return render_template('course_home.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', error_message="Course not found"), 404
    
    if course.teacher_id != user_id:
        return render_template('course_home.html', error_message="You are not the teacher of this course"), 403
    
    # Get poll
    poll = Poll.query.filter_by(id=poll_id, course_code=course_code).first()
    if not poll:
        return render_template('course_home.html', error_message="Poll not found"), 404
    
    # Delete poll (cascade will delete questions and choices)
    db.session.delete(poll)
    db.session.commit()
    
    flash('Poll deleted successfully!')
    return redirect(url_for('poll.teacher_poll_list', course_code=course_code))

@poll_bp.route('/course/<course_code>/poll/<int:poll_id>/submit', methods=['POST'])
def submit_poll(course_code, poll_id):
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
    
    # Get poll
    poll = Poll.query.filter_by(id=poll_id, course_code=course_code).first()
    if not poll:
        return render_template('poll_list.html', course=course, polls=[], error_message="Poll not found"), 404
    
    # Check if user has already responded through submission
    has_responded = QuestionResponse.query.join(Submission).filter(
        QuestionResponse.submission_id == Submission.id,
        Submission.user_id == user_id,
        Submission.poll_id == poll_id
    ).first() is not None
    
    if has_responded:
        return redirect(f'/course/{course_code}/poll?already_submitted=1')
    
    # Get all questions for this poll
    questions = Question.query.filter_by(poll_id=poll_id).all()
    
    # Create submission record
    submission = Submission(
        user_id=user_id,
        poll_id=poll_id
    )
    db.session.add(submission)
    db.session.flush()  # To get the submission ID
    
    # Process answers
    for question in questions:
        answer_key = f"question-{question.id}"
        user_answer = request.form.get(answer_key)
        
        if question.type == 'mcq':
            # Create response for MCQ
            response = QuestionResponse(
                submission_id=submission.id,
                question_id=question.id,
                choice_id=user_answer,  # This could be None if no answer provided
                text_answer=None
            )
            db.session.add(response)
        elif question.type == 'saq':
            # Create response for short answer question
            response = QuestionResponse(
                submission_id=submission.id,
                question_id=question.id,
                choice_id=None,
                text_answer=user_answer  # This could be None if no answer provided
            )
            db.session.add(response)
    
    # Save all changes
    db.session.commit()
    
    # Redirect to poll results page with visibility controls
    return redirect(url_for('poll.get_poll_results', course_code=course_code, poll_id=poll_id))