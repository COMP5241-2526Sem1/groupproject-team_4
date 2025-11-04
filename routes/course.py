from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from models.course import Course
from models.course_enrollment import CourseEnrollment
from models.user import User
from models.submission import Submission
from models.quiz import Quiz
from models.question import Question
from models.choice import Choice
from models.question_response import QuestionResponse
from models.poll import Poll
from database import db

course_bp = Blueprint('course', __name__)
# THIS IS RESTFUL API, NOT A VISABLE WEB PAGE!!!

# Get all available course (not enrolled)
@course_bp.route('/course/available', methods=['GET'])
def get_available_course():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': 'Not logged in'}), 401
    # Enrolled course IDs
    enrolled_ids = [e.course_id for e in CourseEnrollment.query.filter_by(student_id=student_id).all()]
    # Available course (not enrolled and not full)
    # Weekday sorting helper dictionary
    weekday_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    course = Course.query.filter(~Course.id.in_(enrolled_ids)).all()
    course = sorted(course, key=lambda c: (weekday_order.get(c.day_of_week, 99), c.start_time))
    result = []
    for c in course:
        enrolled_count = CourseEnrollment.query.filter_by(course_id=c.id).count()
        result.append({
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'credit': c.credit,
            'capacity': c.capacity,
            'enrolled': enrolled_count,
            'teacher_id': c.teacher_id,
            'day_of_week': c.day_of_week,
            'start_time': str(c.start_time) if c.start_time else '',
            'end_time': str(c.end_time) if c.end_time else ''
        })
    return jsonify(result)

# Get student's enrolled course
@course_bp.route('/course/my', methods=['GET'])
def get_my_course():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': 'Not logged in'}), 401
    enrollments = CourseEnrollment.query.filter_by(student_id=student_id).all()
    # Retrieve all enrolled course objects
    course = [Course.query.get(e.course_id) for e in enrollments]
    weekday_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    course_sorted = sorted(course, key=lambda c: (weekday_order.get(c.day_of_week, 99), c.start_time))
    result = []
    for c in course_sorted:
        result.append({
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'credit': c.credit,
            'capacity': c.capacity,
            'teacher_id': c.teacher_id,
            'day_of_week': c.day_of_week,
            'start_time': str(c.start_time) if c.start_time else '',
            'end_time': str(c.end_time) if c.end_time else ''
        })
    return jsonify(result)

# add
@course_bp.route('/course/add', methods=['POST'])
def add_course():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': 'Not logged in'}), 401
    course_id = request.json.get('course_id')
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'msg': '课程不存在'}), 404
    # 校验是否已选
    if CourseEnrollment.query.filter_by(student_id=student_id, course_id=course_id).first():
        return jsonify({'msg': '已选该课程'}), 400
    # 校验人数
    enrolled_count = CourseEnrollment.query.filter_by(course_id=course_id).count()
    if enrolled_count >= course.capacity:
        return jsonify({'msg': '课程人数已满'}), 400
    # 校验学分和课程数
    enrollments = CourseEnrollment.query.filter_by(student_id=student_id).all()
    total_credits = sum(Course.query.get(e.course_id).credit for e in enrollments)
    if total_credits + course.credit > 18:
        return jsonify({'msg': '学分超限，最多18学分'}), 400
    if len(enrollments) >= 6:
        return jsonify({'msg': '最多只能选6门课程'}), 400
    # 校验时间冲突
    for e in enrollments:
        c2 = Course.query.get(e.course_id)
        if c2.day_of_week == course.day_of_week:
            # 时间有重叠则冲突
            if not (course.end_time <= c2.start_time or course.start_time >= c2.end_time):
                return jsonify({'msg': '课程时间冲突，请选择其他课程'}), 400
    # 添加选课
    new_enroll = CourseEnrollment(course_id=course_id, student_id=student_id)
    db.session.add(new_enroll)
    db.session.commit()
    return jsonify({'msg': '选课成功'})

# drop
@course_bp.route('/course/drop', methods=['POST'])
def drop_course():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': 'Not logged in'}), 401
    course_id = request.json.get('course_id')
    enroll = CourseEnrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if not enroll:
        return jsonify({'msg': 'not enrolled in this course'}), 400
    db.session.delete(enroll)
    db.session.commit()
    return jsonify({'msg': 'course dropped successfully!'})

@course_bp.route('/course/<course_id>/quiz', methods=['GET'])
def get_quiz_list(course_id):
    # Check if course_id is an integer or a code
    course = None
    try:
        # Try to parse as integer ID first
        course_id_int = int(course_id)
        course = Course.query.get(course_id_int)
    except ValueError:
        # If not an integer, try to find by course code
        course = Course.query.filter_by(code=course_id).first()
    
    # If course not found, return error
    if not course:
        return render_template('quiz_list.html', message="Course not found.")
    
    # Use the actual course ID for further processing
    course_id = course.id
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.query.filter_by(
        student_id=user_id, 
        course_id=course_id
    ).first()
    
    if not enrollment:
        return render_template('quiz_list.html', message="You are not enrolled in this course.")
    
    # Get quizzes for the specified course
    quizzes = Quiz.query.filter_by(course_id=course_id).all()
    
    # Format quiz data for template
    quiz_data = []
    for quiz in quizzes:
        # Calculate used_attempts by querying the Submission table
        used_attempts = Submission.query.filter_by(
            student_id=user_id,
            quiz_id=quiz.id
        ).count()
        
        quiz_info = {
            'id': quiz.id,
            'name': quiz.title,
            'used_attempts': used_attempts,
            'max_attempts': quiz.attempt_limit
        }
        quiz_data.append(quiz_info)
    
    # If there are no quizzes, return a message
    if not quiz_data:
        return render_template('quiz_list.html', message="No quizzes available for this course.")
    
    # 获取URL参数中的submitted标志
    submitted = request.args.get('submitted')
    # Return all quizzes, course object and course_id for the template to use
    return render_template('quiz_list.html', quizzes=quiz_data, course=course, course_id=course_id, submitted=submitted)

@course_bp.route('/course/<course_id>/poll', methods=['GET'])
def get_poll_list(course_id):
    # Check if course_id is an integer or a code
    course = None
    try:
        # Try to parse as integer ID first
        course_id_int = int(course_id)
        course = Course.query.get(course_id_int)
    except ValueError:
        # If not an integer, try to find by course code
        course = Course.query.filter_by(code=course_id).first()
    
    # If course not found, return error
    if not course:
        return render_template('poll_list.html', message="Course not found.")
    
    # Use the actual course ID for further processing
    course_id = course.id
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.query.filter_by(
        student_id=user_id, 
        course_id=course_id
    ).first()
    
    if not enrollment:
        return render_template('poll_list.html', message="You are not enrolled in this course.")
    
    # Get polls for the specified course
    polls = Poll.query.filter_by(course_id=course_id).all()
    
    # Format poll data for template
    poll_data = []
    for poll in polls:
        # 检查用户是否已参与该poll（通过检查是否有相关的submission）
        has_responded = db.session.query(Submission).join(QuestionResponse).join(Question).filter(
            Submission.student_id == user_id,
            Question.poll_id == poll.id
        ).first() is not None
        
        poll_info = {
            'id': poll.id,
            'title': poll.title,
            'has_responded': has_responded
        }
        poll_data.append(poll_info)
    
    # If there are no polls, return a message
    if not poll_data:
        return render_template('poll_list.html', message="No polls available.", course=course, course_id=course_id)
    
    # 获取URL参数中的submitted标志
    submitted = request.args.get('submitted')
    # Return all polls, course object and course_id for the template to use
    return render_template('poll_list.html', polls=poll_data, course=course, course_id=course_id, submitted=submitted)

# show quiz info(name user attempt, max attempt) user can choose to start
@course_bp.route('/course/<course_id>/quiz/<int:quiz_id>', methods=['GET'])
def get_quiz_info(course_id, quiz_id):
    # Check if course_id is an integer or a code
    course = None
    try:
        # Try to parse as integer ID first
        course_id_int = int(course_id)
        course = Course.query.get(course_id_int)
    except ValueError:
        # If not an integer, try to find by course code
        course = Course.query.filter_by(code=course_id).first()
    
    # If course not found, return error
    if not course:
        return render_template('quiz_info.html', message="Course not found.")
    
    # Use the actual course ID for further processing
    course_id = course.id
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.query.filter_by(
        student_id=user_id, 
        course_id=course_id
    ).first()
    
    if not enrollment:
        return render_template('quiz_info.html', message="You are not enrolled in this course.")
    
    # Get the specific quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_id=course_id).first()
    
    if not quiz:
        return render_template('quiz_info.html', message="Quiz not found.")
    
    # Calculate used_attempts by querying the Submission table
    used_attempts = Submission.query.filter_by(
        student_id=user_id,
        quiz_id=quiz.id
    ).count()
    
    # Format quiz data for template
    quiz_data = {
        'id': quiz.id,
        'name': quiz.title,
        'description': quiz.description,
        'used_attempts': used_attempts,
        'max_attempts': quiz.attempt_limit
    }
    
    # Return quiz data, course object and course_id for the template to use
    return render_template('quiz_info.html', quiz=quiz_data, course=course, course_id=course_id)


@course_bp.route('/course/<course_id>/quiz/<int:quiz_id>/start', methods=['GET'])  
def start_quiz(course_id, quiz_id):
    # Check if course_id is an integer or a code
    course = None
    try:
        # Try to parse as integer ID first
        course_id_int = int(course_id)
        course = Course.query.get(course_id_int)
    except ValueError:
        # If not an integer, try to find by course code
        course = Course.query.filter_by(code=course_id).first()
    
    # If course not found, return error
    if not course:
        return render_template('quiz_start.html', error_message="Course not found.")
    
    # Use the actual course ID for further processing
    course_id = course.id
    
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.query.filter_by(
        student_id=user_id, 
        course_id=course_id
    ).first()
    
    if not enrollment:
        return render_template('quiz_start.html', error_message="You are not enrolled in this course.")
    
    # Get the specific quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_id=course_id).first()
    
    if not quiz:
        return render_template('quiz_start.html', error_message="Quiz not found.")
    
    # Check attempt limit
    used_attempts = Submission.query.filter_by(
        student_id=user_id,
        quiz_id=quiz.id
    ).count()
    
    if used_attempts >= quiz.attempt_limit:
        # Format quiz data for template even when attempt limit is reached
        quiz_data = {
            'id': quiz.id,
            'name': quiz.title,
            'description': quiz.description,
            'used_attempts': used_attempts,
            'max_attempts': quiz.attempt_limit
        }
        return render_template('quiz_start.html', error_message="You have reached the maximum number of attempts for this quiz.", quiz=quiz_data, course=course, course_id=course_id)
    
    # Get all questions with their choices for the quiz
    questions = []
    for question in quiz.questions:
        question_data = {
            'id': question.id,
            'type': question.type,
            'content': question.content,
            'points': question.points
        }
        
        # If it's an MCQ, include the choices
        if question.type == 'mcq':
            question_data['choices'] = [
                {'id': choice.id, 'content': choice.content}
                for choice in question.choices
            ]
        
        questions.append(question_data)
    
    # Format quiz data for template
    quiz_data = {
        'id': quiz.id,
        'name': quiz.title,
        'description': quiz.description,
        'used_attempts': used_attempts,
        'max_attempts': quiz.attempt_limit
    }
    
    # Render the quiz_start template with questions
    return render_template(
        'quiz_start.html', 
        quiz=quiz_data, 
        course=course, 
        course_id=course_id,
        questions=questions
    )

@course_bp.route('/course/<course_id>/quiz/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(course_id, quiz_id):
    # Check if course_id is an integer or a code
    course = None
    try:
        # Try to parse as integer ID first
        course_id_int = int(course_id)
        course = Course.query.get(course_id_int)
    except ValueError:
        # If not an integer, try to find by course code
        course = Course.query.filter_by(code=course_id).first()
    
    # If course not found, return error
    if not course:
        return render_template('quiz_start.html', error_message="Course not found.")
    
    # Use the actual course ID for further processing
    course_id = course.id
    
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.query.filter_by(
        student_id=user_id, 
        course_id=course_id
    ).first()
    
    if not enrollment:
        return render_template('quiz_start.html', error_message="You are not enrolled in this course.")
    
    # Get the specific quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_id=course_id).first()
    
    if not quiz:
        return render_template('quiz_start.html', error_message="Quiz not found.")
    
    # Check attempt limit before creating submission
    used_attempts = Submission.query.filter_by(
        student_id=user_id,
        quiz_id=quiz.id
    ).count()
    
    if used_attempts >= quiz.attempt_limit:
        return render_template('quiz_start.html', error_message="You have reached the maximum number of attempts for this quiz.")
    
    # Create a new submission record
    submission = Submission(
        student_id=user_id,
        quiz_id=quiz.id
    )
    
    db.session.add(submission)
    db.session.flush()  # Get the submission ID before committing
    
    # Process each question response
    total_score = 0.0
    for question in quiz.questions:
        # Get the user's answer from the form
        answer_key = f'question-{question.id}'
        user_answer = request.form.get(answer_key)
        
        # Create question response with default values
        is_correct = False
        response_content = ''
        user_points = 0.0
        
        if user_answer:
            # Process answered question
            response_content = user_answer
            
            if question.type == 'mcq':
                # For MCQ, check if the selected choice is correct
                try:
                    selected_choice = Choice.query.get(int(user_answer))
                    if selected_choice and selected_choice.is_correct:
                        is_correct = True
                        total_score += question.points
                        user_points = float(question.points)
                    # Store the selected choice content
                    response_content = selected_choice.content if selected_choice else user_answer
                except (ValueError, TypeError):
                    # Invalid choice ID, treat as incorrect
                    pass
            elif question.type == 'saq':
                # For short answer, store the text (grading would typically be manual)
                # For now, we'll mark as not correct since we can't auto-grade
                is_correct = None  # None indicates needs manual grading
                response_content = user_answer.strip()
        else:
            # Process unanswered question
            if question.type == 'mcq':
                is_correct = False  # Explicitly set to False for unanswered MCQ
                response_content = 'Unanswered'
                user_points = 0.0
            elif question.type == 'saq':
                is_correct = None  # Still None for unanswered SAQ (needs manual grading)
                response_content = ''
                user_points = 0.0
        
        # Create the question response record for every question
        question_response = QuestionResponse(
            submission_id=submission.id,
            question_id=question.id,
            content=response_content,
            is_correct=is_correct,
            points=user_points
        )
        
        db.session.add(question_response)
    
    # Update submission grade if it's auto-gradable (all questions are MCQ)
    if quiz.is_graded and all(q.type == 'mcq' for q in quiz.questions):
        submission.grade = total_score
    
    # Commit all changes to the database
    db.session.commit()
    
    # Redirect to quiz list with success message
    return redirect(f'/course/{course_id}/quiz?submitted=1')

# Poll related routes
@course_bp.route('/course/<course_id>/poll/<int:poll_id>', methods=['GET'])
def get_poll_info(course_id, poll_id):
    # Check if course_id is an integer or a code
    course = None
    try:
        # Try to parse as integer ID first
        course_id_int = int(course_id)
        course = Course.query.get(course_id_int)
    except ValueError:
        # If not an integer, try to find by course code
        course = Course.query.filter_by(code=course_id).first()
    
    # If course not found, return error
    if not course:
        return render_template('poll_info.html', message="Course not found.")
    
    # Use the actual course ID for further processing
    course_id = course.id
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.query.filter_by(
        student_id=user_id, 
        course_id=course_id
    ).first()
    
    if not enrollment:
        return render_template('poll_info.html', message="You are not enrolled in this course.")
    
    # Get the specific poll
    poll = Poll.query.get(poll_id)
    
    if not poll:
        return render_template('poll_info.html', message="Poll not found.")
    
    # Check if user has already responded
    has_responded = db.session.query(Submission).join(QuestionResponse).join(Question).filter(
        Submission.student_id == user_id,
        Question.poll_id == poll.id
    ).first() is not None
    
    # Format poll data for template
    poll_data = {
        'id': poll.id,
        'title': poll.title,
        'description': poll.description,
        'has_responded': has_responded
    }
    
    # Return poll data, course object and course_id for the template to use
    return render_template('poll_info.html', poll=poll_data, course=course, course_id=course_id)

@course_bp.route('/course/<course_id>/poll/<int:poll_id>/start', methods=['GET'])
def start_poll(course_id, poll_id):
    # Check if course_id is an integer or a code
    course = None
    try:
        # Try to parse as integer ID first
        course_id_int = int(course_id)
        course = Course.query.get(course_id_int)
    except ValueError:
        # If not an integer, try to find by course code
        course = Course.query.filter_by(code=course_id).first()
    
    # If course not found, return error
    if not course:
        return render_template('poll_start.html', error_message="Course not found.")
    
    # Use the actual course ID for further processing
    course_id = course.id
    
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.query.filter_by(
        student_id=user_id, 
        course_id=course_id
    ).first()
    
    if not enrollment:
        return render_template('poll_start.html', error_message="You are not enrolled in this course.")
    
    # Get the specific poll
    poll = Poll.query.get(poll_id)
    
    if not poll:
        return render_template('poll_start.html', error_message="Poll not found.")
    
    # Check if user has already responded
    has_responded = db.session.query(Submission).join(QuestionResponse).join(Question).filter(
        Submission.student_id == user_id,
        Question.poll_id == poll.id
    ).first() is not None
    
    if has_responded:
        # Format poll data for template even when user has already responded
        poll_data = {
            'id': poll.id,
            'title': poll.title,
            'description': poll.description,
            'has_responded': has_responded
        }
        return render_template('poll_start.html', error_message="You have already responded to this poll.", poll=poll_data, course=course, course_id=course_id)
    
    # Get all questions with their choices for the poll
    questions = []
    for question in poll.questions:
        question_data = {
            'id': question.id,
            'type': question.type,
            'content': question.content
        }
        
        # If it's an MCQ, include the choices
        if question.type == 'mcq':
            question_data['choices'] = [
                {'id': choice.id, 'content': choice.content}
                for choice in question.choices
            ]
        
        questions.append(question_data)
    
    # Format poll data for template
    poll_data = {
        'id': poll.id,
        'title': poll.title,
        'description': poll.description
    }
    
    # Render the poll_start template with questions
    return render_template(
        'poll_start.html', 
        poll=poll_data, 
        course=course, 
        course_id=course_id,
        questions=questions
    )

@course_bp.route('/course/<course_id>/poll/<int:poll_id>/submit', methods=['POST'])
def submit_poll(course_id, poll_id):
    # Check if course_id is an integer or a code
    course = None
    try:
        # Try to parse as integer ID first
        course_id_int = int(course_id)
        course = Course.query.get(course_id_int)
    except ValueError:
        # If not an integer, try to find by course code
        course = Course.query.filter_by(code=course_id).first()
    
    # If course not found, return error
    if not course:
        return render_template('poll_start.html', error_message="Course not found.")
    
    # Use the actual course ID for further processing
    course_id = course.id
    
    # Check if user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check if user is enrolled in this course
    enrollment = CourseEnrollment.query.filter_by(
        student_id=user_id, 
        course_id=course_id
    ).first()
    
    if not enrollment:
        return render_template('poll_start.html', error_message="You are not enrolled in this course.")
    
    # Get the specific poll
    poll = Poll.query.get(poll_id)
    
    if not poll:
        return render_template('poll_start.html', error_message="Poll not found.")
    
    # Check if user has already responded
    has_responded = db.session.query(Submission).join(QuestionResponse).join(Question).filter(
        Submission.student_id == user_id,
        Question.poll_id == poll.id
    ).first() is not None
    
    if has_responded:
        return render_template('poll_start.html', error_message="You have already responded to this poll.")
    
    # Create a new submission record for the poll
    submission = Submission(
        student_id=user_id,
        poll_id=poll_id  # Using poll_id instead of quiz_id
    )
    
    db.session.add(submission)
    db.session.flush()  # Get the submission ID before committing
    
    # Process each question response
    for question in poll.questions:
        # Get the user's answer from the form
        answer_key = f'question-{question.id}'
        user_answer = request.form.get(answer_key)
        
        # For polls, we just store the response without grading
        response_content = ''
        is_correct = None
        user_points = 0.0
        
        if user_answer:
            # Process answered question
            if question.type == 'mcq':
                # For MCQ, get the selected choice content
                try:
                    selected_choice = Choice.query.get(int(user_answer))
                    if selected_choice and selected_choice.question_id == question.id:
                        response_content = selected_choice.content
                except (ValueError, TypeError):
                    # Invalid choice ID
                    response_content = user_answer
            elif question.type == 'saq':
                # For short answer, store the text
                response_content = user_answer.strip()
        else:
            # Process unanswered question
            response_content = 'Unanswered'
        
        # Create the question response record for every question
        question_response = QuestionResponse(
            submission_id=submission.id,
            question_id=question.id,
            content=response_content,
            is_correct=is_correct,
            points=user_points
        )
        
        db.session.add(question_response)
    
    # Commit all changes to the database
    db.session.commit()
    
    # Redirect to poll list with success message
    return redirect(f'/course/{course_id}/poll?submitted=1')