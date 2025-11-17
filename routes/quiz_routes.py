from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template, flash
from models.course import Course
from models.course_enrollment import CourseEnrollment
from models.user import User
from models.submission import Submission
from models.quiz import Quiz
from models.question import Question
from models.choice import Choice
from models.question_response import QuestionResponse
from models.attempt import Attempt
from models.quiz_grade import QuizGrade
from database import db
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

def calculate_and_save_quiz_grade(quiz_id, student_id, submission_id):
    """Calculate quiz grade based on submission and save to QuizGrade table"""
    try:
        # Get the submission
        submission = Submission.query.get(submission_id)
        if not submission:
            return False, "Submission not found"
        
        # Get the quiz
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return False, "Quiz not found"
        
        # Get all questions for this quiz
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        
        # Calculate total points possible
        total_points_possible = sum(q.points for q in questions)
        
        # Get all responses for this submission
        responses = QuestionResponse.query.filter_by(submission_id=submission_id).all()
        
        # Calculate points earned
        points_earned = 0
        for response in responses:
            if response.is_correct:
                question = Question.query.get(response.question_id)
                if question:
                    points_earned += question.points
        
        # Calculate percentage
        percentage = (points_earned / total_points_possible * 100) if total_points_possible > 0 else 0
        
        # Check if quiz grade already exists
        existing_grade = QuizGrade.query.filter_by(quiz_id=quiz_id, student_id=student_id).first()
        
        if existing_grade:
            # Update existing grade
            existing_grade.points_earned = points_earned
            existing_grade.points_possible = total_points_possible
            existing_grade.percentage = percentage
            existing_grade.submission_id = submission_id
            existing_grade.updated_at = datetime.utcnow()
        else:
            # Create new quiz grade
            quiz_grade = QuizGrade(
                quiz_id=quiz_id,
                student_id=student_id,
                points_earned=points_earned,
                points_possible=total_points_possible,
                percentage=percentage,
                submission_id=submission_id
            )
            db.session.add(quiz_grade)
        
        db.session.commit()
        return True, "Quiz grade calculated and saved successfully"
        
    except Exception as e:
        db.session.rollback()
        return False, f"Error calculating quiz grade: {str(e)}"

@quiz_bp.route('/course/<course_code>/quiz', methods=['GET'])
def get_quiz_list(course_code):
    # First, verify if the course exists
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', course=None, error_message="Course not found"), 404
    
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
        
        # Get quiz grade if available
        quiz_grade = QuizGrade.query.filter_by(quiz_id=quiz.id, student_id=user_id).first()
        
        # Check if quiz is currently available (within start and end datetime)
        current_time = datetime.now()
        is_available = True
        if quiz.start_datetime and current_time < quiz.start_datetime:
            is_available = False
        if quiz.end_datetime and current_time > quiz.end_datetime:
            is_available = False
        
        quiz_data.append({
            'id': quiz.id,
            'name': quiz.name,
            'description': quiz.description,
            'has_responded': has_responded,
            'used_attempts': attempt_count,
            'max_attempts': quiz.attempt_limit,
            'start_datetime': quiz.start_datetime,
            'end_datetime': quiz.end_datetime,
            'is_available': is_available,
            'grade': quiz_grade
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
        return render_template('course_home.html', course=None, error_message="Course not found"), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment or teacher ownership
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    user = User.query.get(user_id)
    is_teacher = user and user.role == 'teacher'
    is_course_teacher = is_teacher and course.teacher_id == user_id
    
    # Redirect teachers to teacher-specific route
    if is_course_teacher:
        return redirect(url_for('teacher_quiz.teacher_view_quiz', course_code=course_code, quiz_id=quiz_id))
    
    if not enrollment and not is_course_teacher:
        return render_template('course_home.html', course=course, error_message="You are not enrolled in this course and you are not the course teacher"), 403
    
    # Get quiz details
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_info.html', course=None, quiz=None, quizzes=[], course_code=course_code, error_message="Quiz not found"), 404
    
    # Get attempt count
    attempt_count = Attempt.query.filter_by(quiz_id=quiz_id, user_id=user_id).count()
    
    # Check if user is teacher (teachers have unlimited attempts)
    user = User.query.get(user_id)
    is_teacher = user and user.role == 'teacher'
    
    # Check if user can attempt again (teachers always can)
    can_attempt = is_teacher or not quiz.attempt_limit or attempt_count < quiz.attempt_limit
    
    # Show appropriate message for students who can't access quiz feedback
    message = None
    
    # Check if quiz has submissions but no remaining attempts
    if not is_teacher and attempt_count > 0 and not can_attempt:
        message = "You have completed this quiz and used all available attempts."
    
    # Check if quiz has no submissions and no remaining attempts  
    elif not is_teacher and attempt_count == 0 and not can_attempt:
        message = "You have used all your quiz attempts and have no submissions to view results."
    
    # Check if quiz has submissions and can still attempt (partial completion)
    elif not is_teacher and attempt_count > 0 and can_attempt:
        # Check if student has submissions but limited feedback is available
        if not quiz.after_submitted_student_response_visible:
            message = f"You have attempted this quiz {attempt_count} time(s) and have {quiz.attempt_limit - attempt_count} attempt(s) remaining. Quiz feedback is limited - you can view results but not your detailed responses."
        else:
            message = f"You have attempted this quiz {attempt_count} time(s) and have {quiz.attempt_limit - attempt_count} attempt(s) remaining."
    
    # Check if student has submissions but limited feedback is available (and no remaining attempts)
    elif not is_teacher and attempt_count > 0 and not quiz.after_submitted_student_response_visible:
        message = "Quiz feedback is limited for this completed quiz. You can view results but not your detailed responses."
    
    # Check if no feedback is available (regardless of attempt status)
    elif not is_teacher and not quiz.after_submitted_question_visible and not quiz.after_submitted_student_response_visible and not quiz.after_submitted_sample_response_visible and not quiz.after_submitted_class_response_visible:
        if attempt_count > 0:
            message = "Quiz feedback is not available for this completed quiz."
        else:
            message = "Quiz feedback is not available for this quiz."
    
    # Check if user has submissions to show results preview
    submission = Submission.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
    has_submission = submission is not None
    
    # Prepare results preview data when quiz is completed and visibility allows
    results_preview = None
    if has_submission and not can_attempt and (quiz.after_submitted_question_visible or quiz.after_submitted_student_response_visible or quiz.after_submitted_sample_response_visible or quiz.after_submitted_class_response_visible):
        # Get user's responses
        responses = QuestionResponse.query.filter_by(submission_id=submission.id).all()
        
        # Get class statistics if class response is visible
        class_stats = None
        if quiz.after_submitted_class_response_visible:
            all_submissions = Submission.query.filter_by(quiz_id=quiz_id).all()
            if all_submissions:
                total_students = len(all_submissions)
                total_score = sum(sub.grade for sub in all_submissions if sub.grade is not None)
                average_score = total_score / total_students if total_students > 0 else 0
                class_stats = {
                    'total_students': total_students,
                    'average_score': average_score
                }
        
        # Prepare results preview
        results_preview = {
            'score': submission.grade,
            'submitted_at': submission.submitted_at,
            'visibility': {
                'question_visible': quiz.after_submitted_question_visible,
                'student_response_visible': quiz.after_submitted_student_response_visible,
                'sample_response_visible': quiz.after_submitted_sample_response_visible,
                'class_response_visible': quiz.after_submitted_class_response_visible
            },
            'class_statistics': class_stats,
            'questions': []
        }
        
        # Add question details based on visibility
        for response in responses:
            question = Question.query.get(response.question_id)
            if question:
                question_data = {
                    'id': question.id,
                    'content': question.content if quiz.after_submitted_question_visible else None,
                    'type': question.type,
                    'points': question.points,
                    'user_answer': response.text_answer if quiz.after_submitted_student_response_visible else None,
                    'is_correct': response.is_correct if quiz.after_submitted_student_response_visible else None,
                    'correct_answer': None
                }
                
                # Add correct answer if sample response is visible
                if quiz.after_submitted_sample_response_visible and question.type == 'mcq':
                    correct_choice = next((choice for choice in question.choices if choice.is_correct), None)
                    if correct_choice:
                        question_data['correct_answer'] = correct_choice.content
                elif quiz.after_submitted_sample_response_visible and question.type == 'short_answer':
                    # For short answer, we might want to show the expected answer
                    # This would need to be implemented based on your short answer model
                    pass
                
                results_preview['questions'].append(question_data)
    
    # Show questions based on visibility parameters when used_attempts > 0
    elif attempt_count > 0 and (quiz.after_submitted_question_visible or quiz.after_submitted_student_response_visible or quiz.after_submitted_sample_response_visible or quiz.after_submitted_class_response_visible):
        # Get all questions for this quiz
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        
        # Prepare results preview with questions based on visibility
        results_preview = {
            'score': None,  # No submission yet, so no score
            'submitted_at': None,
            'visibility': {
                'question_visible': quiz.after_submitted_question_visible,
                'student_response_visible': quiz.after_submitted_student_response_visible,
                'sample_response_visible': quiz.after_submitted_sample_response_visible,
                'class_response_visible': quiz.after_submitted_class_response_visible
            },
            'class_statistics': None,
            'questions': []
        }
        
        # Add questions based on visibility parameters
        for question in questions:
            question_data = {
                'id': question.id,
                'content': question.content if quiz.after_submitted_question_visible else None,
                'type': question.type,
                'points': question.points,
                'user_answer': None,
                'is_correct': None,
                'correct_answer': None
            }
            
            # Add correct answer if sample response is visible
            if quiz.after_submitted_sample_response_visible and question.type == 'mcq':
                correct_choice = next((choice for choice in question.choices if choice.is_correct), None)
                if correct_choice:
                    question_data['correct_answer'] = correct_choice.content
            elif quiz.after_submitted_sample_response_visible and question.type == 'short_answer':
                # For short answer, we might want to show the expected answer
                pass
            
            results_preview['questions'].append(question_data)
    
    # Prepare questions with choices (for MCQ)
    quiz_data = {
        'id': quiz.id,
        'name': quiz.name,
        'description': quiz.description,
        'used_attempts': attempt_count,
        'max_attempts': quiz.attempt_limit,
        'can_attempt': can_attempt,
        'has_submission': has_submission,
        'questions': []
    }

    return render_template('quiz_info.html', course=course, quiz=quiz_data, course_code=course_code, message=message, results_preview=results_preview)

@quiz_bp.route('/course/<course_code>/quiz/<int:quiz_id>/start', methods=['GET'])
def start_quiz(course_code, quiz_id):
    # Verify course exists
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', course=None, error_message="Course not found"), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment or teacher ownership
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    user = User.query.get(user_id)
    is_teacher = user and user.role == 'teacher'
    is_course_teacher = is_teacher and course.teacher_id == user_id
    
    # Redirect teachers to teacher-specific route
    if is_course_teacher:
        return redirect(url_for('teacher_quiz.teacher_start_quiz', course_code=course_code, quiz_id=quiz_id))
    
    if not enrollment and not is_course_teacher:
        return render_template('course_home.html', course=course, error_message="You are not enrolled in this course and you are not the course teacher"), 403
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_list.html', course=course, quizzes=[], error_message="Quiz not found", course_code=course_code), 404
    
    # Check if quiz is currently available (within start and end datetime)
    current_time = datetime.now()
    is_available = True
    if quiz.start_datetime and current_time < quiz.start_datetime:
        is_available = False
    if quiz.end_datetime and current_time > quiz.end_datetime:
        is_available = False
    
    # Get attempt count before using it
    attempt_count = Attempt.query.filter_by(quiz_id=quiz_id, user_id=user_id).count()
    
    if not is_available:
        return render_template('quiz_info.html', course=course, quiz={
            'id': quiz.id,
            'name': quiz.name,
            'description': quiz.description,
            'used_attempts': attempt_count,
            'max_attempts': quiz.attempt_limit,
            'can_attempt': False,
            'start_datetime': quiz.start_datetime,
            'end_datetime': quiz.end_datetime
        }, course_code=course_code, error_message="This quiz is not currently available"), 400
    
    # Check if user has already submitted
    has_responded = Submission.query.filter_by(quiz_id=quiz_id, user_id=user_id).first() is not None
    
    # Check if user can attempt again (teachers always can)
    is_teacher = user and user.role == 'teacher'
    
    if not is_teacher and quiz.attempt_limit and attempt_count >= quiz.attempt_limit:
        return render_template('quiz_info.html', course=course, quiz={
            'id': quiz.id,
            'name': quiz.name,
            'description': quiz.description,
            'has_responded': has_responded,
            'used_attempts': attempt_count,
            'max_attempts': quiz.attempt_limit,
            'can_attempt': False,
            'start_datetime': quiz.start_datetime,
            'end_datetime': quiz.end_datetime
        }, course_code=course_code, error_message="You have reached the maximum number of attempts for this quiz"), 400
    
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
        'start_datetime': quiz.start_datetime,
        'end_datetime': quiz.end_datetime,
        'questions': [{
            'id': q.id,
            'content': q.content,
            'type': q.type,
            'points': q.points,
            'choices': [{'id': c.id, 'content': c.content} for c in q.choices] if q.type == 'mcq' else []
        } for q in questions]
    }
    
    return render_template('quiz_start.html', course=course, quiz=quiz_data, course_code=course_code)

@quiz_bp.route('/course/<course_code>/quiz/<int:quiz_id>/results', methods=['GET'])
def get_quiz_results(course_code, quiz_id):
    # Verify course exists
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', course=None, error_message="Course not found"), 404
    
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    if not enrollment:
        return render_template('course_home.html', course=course, error_message="You are not enrolled in this course"), 403
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_list.html', course=course, quizzes=[], error_message="Quiz not found", course_code=course_code), 404
    
    # Check if user is a teacher
    user = User.query.get(user_id)
    is_teacher = user.role == 'teacher'
    
    # Check if user has any submissions
    submission_count = Submission.query.filter_by(quiz_id=quiz_id, user_id=user_id).count()
    
    # Redirect students with no submissions back to quiz list
    if not is_teacher and submission_count == 0:
        return redirect(url_for('quiz.get_quiz_list', course_code=course_code))
    
    # Get user's submission
    submission = Submission.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
    if not submission:
        return render_template('quiz_results.html', course=course, quiz=quiz, error_message="No submission found for this quiz. You need to complete the quiz before viewing results.", course_code=course_code), 404
    
    # Get all question responses for this submission
    responses = QuestionResponse.query.filter_by(submission_id=submission.id).all()
    
    # Check if any feedback is visible
    has_visible_feedback = (
        quiz.after_submitted_question_visible or 
        quiz.after_submitted_student_response_visible or 
        quiz.after_submitted_sample_response_visible or 
        quiz.after_submitted_class_response_visible
    )
    
    if not has_visible_feedback:
        return render_template('quiz_results.html', course=course, quiz=quiz, error_message="Quiz feedback is not available for this quiz. Contact your teacher for more information.", course_code=course_code), 200
    
    # Prepare results data based on visibility settings
    results_data = {
        'id': quiz.id,
        'name': quiz.name,
        'description': quiz.description,
        'score': submission.grade,
        'submitted_at': submission.submitted_at,
        'visibility': {
            'question_visible': quiz.after_submitted_question_visible,
            'student_response_visible': quiz.after_submitted_student_response_visible,
            'sample_response_visible': quiz.after_submitted_sample_response_visible,
            'class_response_visible': quiz.after_submitted_class_response_visible
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
            'points': question.points,
            'user_answer': None,
            'is_correct': None,
            'correct_answer': None
        }
        
        # Show question content if visible
        if quiz.after_submitted_question_visible:
            question_data['content'] = question.content
        else:
            question_data['content'] = "[Question content hidden]"
        
        # Show student response if visible
        if quiz.after_submitted_student_response_visible:
            if question.type == 'mcq':
                if response.choice_id:
                    choice = Choice.query.get(response.choice_id)
                    if choice:
                        question_data['user_answer'] = choice.content
                        question_data['is_correct'] = response.is_correct
            elif question.type == 'saq':
                question_data['user_answer'] = response.text_answer
        else:
            question_data['user_answer'] = "[Your response is hidden]"
        
        # Show correct answer if visible
        if quiz.after_submitted_sample_response_visible and question.type == 'mcq':
            correct_choice = Choice.query.filter_by(question_id=question.id, is_correct=True).first()
            if correct_choice:
                question_data['correct_answer'] = correct_choice.content
        
        results_data['questions'].append(question_data)
    
    # Get class statistics if visible
    if quiz.after_submitted_class_response_visible:
        all_submissions = Submission.query.filter_by(quiz_id=quiz_id).all()
        total_students = len(all_submissions)
        if total_students > 0:
            total_score = sum(sub.grade for sub in all_submissions)
            average_score = total_score / total_students
            results_data['class_statistics'] = {
                'total_students': total_students,
                'average_score': average_score
            }
    
    return render_template('quiz_results.html', course=course, quiz=results_data, course_code=course_code)


# Teacher quiz management routes
@quiz_bp.route('/teacher/course/<course_code>/quiz', methods=['GET'])
def teacher_quiz_list(course_code):
    # Check if user is logged in and is a teacher
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if not user or user.role != 'teacher':
        return render_template('course_home.html', course=None, error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.get(course_code)
    if not course:
        return render_template('course_home.html', course=None, error_message="Course not found"), 404
    
    if course.teacher_id != user_id:
        return render_template('course_home.html', course=course, error_message="You are not the teacher of this course"), 403
    
    # Get all quizzes for the course
    quizzes = Quiz.query.filter_by(course_code=course_code).all()
    
    return render_template('teacher_quiz_list.html', course=course, quizzes=quizzes)

@quiz_bp.route('/teacher/course/<course_code>/quiz/create', methods=['GET', 'POST'])
def teacher_create_quiz(course_code):
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
        # Calculate total points from questions first
        total_points = 0
        question_prefix = f'questions['
        
        # Parse form data to calculate total points
        for key, value in request.form.items():
            if key.startswith(question_prefix):
                parts = key.split('][')
                if len(parts) >= 2:
                    field_name = parts[1].replace(']', '')
                    if field_name == 'points':
                        total_points += int(value) if value.isdigit() else 0
        
        # Create new quiz
        quiz = Quiz(
            course_code=course_code,
            name=request.form['name'],
            description=request.form['description'],
            created_by=user_id,
            duration=int(request.form.get('duration', 30)),
            attempt_limit=int(request.form.get('attempt_limit', 5)),
            point=total_points,  # Use calculated total points
            point_in_course=int(request.form.get('point_in_course', 0)),
            # Visibility settings
            after_submitted_question_visible=request.form.get('question_visible', 'false') == 'true',
            after_submitted_student_response_visible=request.form.get('student_response_visible', 'false') == 'true',
            after_submitted_sample_response_visible=request.form.get('sample_response_visible', 'false') == 'true',
            after_submitted_class_response_visible=request.form.get('class_response_visible', 'false') == 'true'
        )
        
        # Handle start and end datetime
        start_datetime_str = request.form.get('start_datetime')
        end_datetime_str = request.form.get('end_datetime')
        
        if start_datetime_str:
            quiz.start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')
        else:
            quiz.start_datetime = None
            
        if end_datetime_str:
            quiz.end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M')
        else:
            quiz.end_datetime = None
        
        db.session.add(quiz)
        db.session.flush()  # This assigns the quiz.id
        
        # Process questions
        # Parse form data to extract questions
        question_prefix = f'questions['
        questions_dict = {}
        
        for key, value in request.form.items():
            if key.startswith(question_prefix):
                # Parse keys like "questions[1][type]" or "questions[1][content]"
                parts = key.split('][')
                if len(parts) >= 2:
                    question_num = parts[0].replace('questions[', '')
                    field_name = parts[1].replace(']', '')
                    
                    if question_num not in questions_dict:
                        questions_dict[question_num] = {}
                    
                    questions_dict[question_num][field_name] = value
        
        # Process parsed questions
        for question_num, question_data in questions_dict.items():
            if 'type' in question_data and 'content' in question_data:
                # Create question
                question = Question(
                    quiz_id=quiz.id,
                    type=question_data['type'],
                    content=question_data['content'],
                    points=int(question_data.get('points', 1))
                )
                db.session.add(question)
                db.session.flush()  # This assigns the question.id
                
                # Handle question type specific data
                if question_data['type'] == 'mcq':
                    # Process choices
                    correct_choice = question_data.get('correct_choice')
                    
                    # Find all choice fields for this question
                    choice_prefix = f'questions[{question_num}][choices]'
                    for choice_key, choice_content in request.form.items():
                        if choice_key.startswith(choice_prefix) and choice_content.strip():
                            # Extract choice number
                            choice_num = choice_key.split('][')[2].replace(']', '') if len(choice_key.split('][')) >= 3 else '1'
                            
                            choice = Choice(
                                question_id=question.id,
                                content=choice_content.strip(),
                                is_correct=(str(choice_num) == str(correct_choice))
                            )
                            db.session.add(choice)
                
                elif question_data['type'] == 'saq':
                    # Handle short answer question
                    expected_answer = question_data.get('expected_answer', '').strip()
                    if expected_answer:
                        # For SAQ, we can store the expected answer in a ShortAnswer model
                        # or handle it differently based on requirements
                        pass
        
        db.session.commit()
        
        flash('Quiz created successfully!')
        return redirect(url_for('quiz.teacher_quiz_list', course_code=course_code))
    
    return render_template('teacher_create_quiz.html', course=course)

@quiz_bp.route('/teacher/course/<course_code>/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
def teacher_edit_quiz(course_code, quiz_id):
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
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('course_home.html', course=course, error_message="Quiz not found"), 404
    
    if request.method == 'POST':
        # Calculate total points from questions first
        total_points = 0
        question_prefix = f'questions['
        
        # Parse form data to calculate total points
        for key, value in request.form.items():
            if key.startswith(question_prefix):
                parts = key.split('][')
                if len(parts) >= 2:
                    field_name = parts[1].replace(']', '')
                    if field_name == 'points':
                        total_points += int(value) if value.isdigit() else 0
        
        # Update quiz
        quiz.name = request.form['name']
        quiz.description = request.form['description']
        quiz.duration = int(request.form.get('duration', 30))
        quiz.attempt_limit = int(request.form.get('attempt_limit', 5))
        quiz.point = total_points  # Use calculated total points
        quiz.point_in_course = int(request.form.get('point_in_course', 0))
        
        # Handle start and end datetime
        start_datetime_str = request.form.get('start_datetime')
        end_datetime_str = request.form.get('end_datetime')
        
        if start_datetime_str:
            quiz.start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')
        else:
            quiz.start_datetime = None
            
        if end_datetime_str:
            quiz.end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M')
        else:
            quiz.end_datetime = None
        
        # Visibility settings
        quiz.after_submitted_question_visible = request.form.get('question_visible', 'false') == 'true'
        quiz.after_submitted_student_response_visible = request.form.get('student_response_visible', 'false') == 'true'
        quiz.after_submitted_sample_response_visible = request.form.get('sample_response_visible', 'false') == 'true'
        quiz.after_submitted_class_response_visible = request.form.get('class_response_visible', 'false') == 'true'
        
        # Process questions
        existing_question_ids = set()
        question_data = {}
        
        # Parse form data to extract question information
        for key, value in request.form.items():
            if key.startswith('questions['):
                # Parse keys like "questions[1][type]" or "questions[1][content]"
                parts = key.split('][')
                if len(parts) >= 2:
                    question_num = parts[0].replace('questions[', '')
                    field_name = parts[1].replace(']', '')
                    
                    if question_num not in question_data:
                        question_data[question_num] = {}
                    
                    if field_name == 'choices' and len(parts) >= 3:
                        # Handle choice data: questions[1][choices][1]
                        choice_num = parts[2].replace(']', '')
                        if 'choices' not in question_data[question_num]:
                            question_data[question_num]['choices'] = {}
                        question_data[question_num]['choices'][choice_num] = value
                    elif field_name == 'correct_choice':
                        question_data[question_num]['correct_choice'] = value
                    else:
                        question_data[question_num][field_name] = value
        
        # Process each question
        for question_num, data in question_data.items():
            question_id = data.get('id')
            question_type = data.get('type')
            question_content = data.get('content')
            question_points = int(data.get('points', 10))
            
            if question_id:
                # Update existing question
                question = Question.query.filter_by(id=question_id, quiz_id=quiz_id).first()
                if question:
                    question.type = question_type
                    question.content = question_content
                    question.points = question_points
                    existing_question_ids.add(question_id)
                    
                    # Update choices for MCQ questions
                    if question_type == 'mcq' and 'choices' in data:
                        # Remove existing choices
                        Choice.query.filter_by(question_id=question_id).delete()
                        
                        # Add new choices
                        correct_choice_num = data.get('correct_choice')
                        for choice_num, choice_content in data['choices'].items():
                            if choice_content.strip():
                                choice = Choice(
                                    question_id=question_id,
                                    content=choice_content.strip(),
                                    is_correct=(choice_num == correct_choice_num)
                                )
                                db.session.add(choice)
            else:
                # Create new question
                question = Question(
                    quiz_id=quiz_id,
                    type=question_type,
                    content=question_content,
                    points=question_points
                )
                db.session.add(question)
                db.session.flush()  # This assigns the question.id
                
                # Add choices for MCQ questions
                if question_type == 'mcq' and 'choices' in data:
                    correct_choice_num = data.get('correct_choice')
                    for choice_num, choice_content in data['choices'].items():
                        if choice_content.strip():
                            choice = Choice(
                                question_id=question.id,
                                content=choice_content.strip(),
                                is_correct=(choice_num == correct_choice_num)
                            )
                            db.session.add(choice)
        
        # Handle questions that are no longer in the form
        for question in quiz.questions:
            if question.id not in existing_question_ids:
                # Check if this question has any responses
                has_responses = QuestionResponse.query.filter_by(question_id=question.id).count() > 0
                
                if has_responses:
                    # Skip deletion for questions with existing responses to avoid foreign key violations
                    # Instead, we could add an 'is_active' field to the Question model in the future
                    # For now, we'll leave the question as-is if it has responses
                    continue
                else:
                    # Safe to delete questions without responses
                    db.session.delete(question)
        
        db.session.commit()
        
        flash('Quiz updated successfully!')
        return redirect(url_for('quiz.teacher_quiz_list', course_code=course_code))
    
    return render_template('teacher_edit_quiz.html', course=course, quiz=quiz)

@quiz_bp.route('/teacher/course/<course_code>/quiz/<int:quiz_id>/questions', methods=['GET'])
def get_quiz_questions(course_code, quiz_id):
    # Check if user is logged in and is a teacher
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(user_id)
    if not user or user.role != 'teacher':
        return jsonify({'error': 'Not authorized'}), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.get(course_code)
    if not course:
        return jsonify({'error': 'Course not found'}), 404
    
    if course.teacher_id != user_id:
        return jsonify({'error': 'Not authorized for this course'}), 403
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Get all questions with their choices
    questions = []
    for question in quiz.questions:
        question_data = {
            'id': question.id,
            'type': question.type,
            'content': question.content,
            'points': question.points,
            'choices': []
        }
        
        # Add choices for MCQ questions
        if question.type == 'mcq':
            for choice in question.choices:
                question_data['choices'].append({
                    'id': choice.id,
                    'content': choice.content,
                    'is_correct': choice.is_correct
                })
        
        questions.append(question_data)
    
    return jsonify({'questions': questions})

@quiz_bp.route('/teacher/course/<course_code>/quiz/<int:quiz_id>/delete', methods=['POST'])
def teacher_delete_quiz(course_code, quiz_id):
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
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('course_home.html', error_message="Quiz not found"), 404
    
    # Delete all related data before deleting the quiz
    # 1. Delete all question responses for submissions related to this quiz
    submissions = Submission.query.filter_by(quiz_id=quiz_id).all()
    for submission in submissions:
        # Delete all question responses for this submission
        QuestionResponse.query.filter_by(submission_id=submission.id).delete()
    
    # 2. Delete all submissions for this quiz
    Submission.query.filter_by(quiz_id=quiz_id).delete()
    
    # 3. Delete all attempts for this quiz
    Attempt.query.filter_by(quiz_id=quiz_id).delete()
    
    # 4. Delete quiz (cascade will delete questions and choices)
    db.session.delete(quiz)
    db.session.commit()
    
    flash('Quiz deleted successfully!')
    return redirect(url_for('quiz.teacher_quiz_list', course_code=course_code))

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
    
    # Check if user is teacher and course teacher
    user = User.query.get(user_id)
    is_teacher = user and user.role == 'teacher'
    is_course_teacher = is_teacher and course.teacher_id == user_id
    
    # Redirect teachers to teacher-specific route
    if is_course_teacher:
        return redirect(url_for('teacher_quiz.teacher_submit_quiz', course_code=course_code, quiz_id=quiz_id))
    
    # Check enrollment for students
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    if not enrollment:
        return render_template('course_home.html', course=course, error_message="You are not enrolled in this course"), 403
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_list.html', course=course, quizzes=[], error_message="Quiz not found"), 404
    
    # Get current attempt ID from session
    attempt_id = session.get('current_attempt_id')
    if not attempt_id:
        return render_template('quiz_start.html', course=course, quiz=quiz, error_message="No active quiz attempt found", course_code=course_code), 400
    
    # Get the attempt
    attempt = Attempt.query.filter_by(id=attempt_id, user_id=user_id, quiz_id=quiz_id).first()
    if not attempt:
        return render_template('quiz_start.html', course=course, quiz=quiz, error_message="Invalid quiz attempt", course_code=course_code), 400
    
    # Get all questions for this quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Process answers first to calculate scores
    total_points = 0
    all_answers_correct = True
    
    # Create submission record first
    submission = Submission(
        user_id=user_id,
        quiz_id=quiz_id
    )
    db.session.add(submission)
    db.session.flush()  # This assigns the submission.id
    
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
    
    # Update submission with final grade
    submission.grade = total_points
    
    # Update attempt with score
    attempt.score = total_points
    attempt.is_completed = True
    
    # Save all changes
    db.session.commit()
    
    # Calculate and save quiz grade
    success, message = calculate_and_save_quiz_grade(quiz_id, user_id, submission.id)
    if not success:
        print(f"Warning: {message}")
    
    # Clear the current attempt from session
    if 'current_attempt_id' in session:
        del session['current_attempt_id']
    
    # Redirect to quiz results page with success message
    flash('Submission Success', 'success')
    return redirect(url_for('quiz.get_quiz_results', course_code=course_code, quiz_id=quiz_id))

@quiz_bp.route('/course/<course_code>/quiz/<int:quiz_id>/grade', methods=['GET'])
def get_quiz_grade(course_code, quiz_id):
    """Get the quiz grade for the current student"""
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    if not enrollment:
        return jsonify({'error': 'Not enrolled in this course'}), 403
    
    # Get quiz grade
    quiz_grade = QuizGrade.query.filter_by(quiz_id=quiz_id, student_id=user_id).first()
    
    if not quiz_grade:
        return jsonify({'error': 'No grade found for this quiz'}), 404
    
    return jsonify({
        'quiz_id': quiz_grade.quiz_id,
        'student_id': quiz_grade.student_id,
        'points_earned': quiz_grade.points_earned,
        'points_possible': quiz_grade.points_possible,
        'percentage': quiz_grade.percentage,
        'submission_id': quiz_grade.submission_id,
        'created_at': quiz_grade.created_at.isoformat(),
        'updated_at': quiz_grade.updated_at.isoformat()
    })

@quiz_bp.route('/course/<course_code>/quiz/grades', methods=['GET'])
def get_all_quiz_grades(course_code):
    """Get all quiz grades for the current student in this course"""
    # Check user is logged in
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    # Check enrollment
    enrollment = CourseEnrollment.query.filter_by(student_id=user_id, course_code=course_code).first()
    if not enrollment:
        return jsonify({'error': 'Not enrolled in this course'}), 403
    
    # Get all quizzes for this course
    quizzes = Quiz.query.filter_by(course_code=course_code).all()
    
    # Get grades for all quizzes
    grades = []
    for quiz in quizzes:
        quiz_grade = QuizGrade.query.filter_by(quiz_id=quiz.id, student_id=user_id).first()
        if quiz_grade:
            grades.append({
                'quiz_id': quiz_grade.quiz_id,
                'quiz_name': quiz.name,
                'points_earned': quiz_grade.points_earned,
                'points_possible': quiz_grade.points_possible,
                'percentage': quiz_grade.percentage,
                'submission_id': quiz_grade.submission_id,
                'created_at': quiz_grade.created_at.isoformat(),
                'updated_at': quiz_grade.updated_at.isoformat()
            })
    
    return jsonify({'grades': grades})

@quiz_bp.route('/teacher/course/<course_code>/quiz/<int:quiz_id>/grading', methods=['GET'])
def teacher_grade_quiz(course_code, quiz_id):
    """Teacher grading page for short answer questions"""
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
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('course_home.html', course=course, error_message="Quiz not found"), 404
    
    # Get all short answer questions for this quiz
    saq_questions = Question.query.filter_by(quiz_id=quiz_id, type='saq').all()
    
    # Get all students enrolled in the course
    enrollments = CourseEnrollment.query.filter_by(course_code=course_code).all()
    student_ids = [enrollment.student_id for enrollment in enrollments]
    students = User.query.filter(User.id.in_(student_ids)).all()
    
    # Get all submissions for this quiz
    submissions = Submission.query.filter_by(quiz_id=quiz_id).all()
    submission_dict = {sub.user_id: sub for sub in submissions}
    
    # Get all question responses for SAQ questions
    saq_data = []
    for question in saq_questions:
        question_responses = []
        for student in students:
            # Get submission for this student (may be None if no submission)
            submission = submission_dict.get(student.id)
            
            # Get response for this question (may be None if student didn't answer)
            response = None
            if submission:
                response = QuestionResponse.query.filter_by(
                    submission_id=submission.id,
                    question_id=question.id
                ).first()
            
            # Always include the student, even if they have no submission or didn't answer
            question_responses.append({
                'student': student,
                'response': response,  # May be None
                'submission_id': submission.id if submission else None
            })
        
        if question_responses:
            saq_data.append({
                'question': question,
                'responses': question_responses
            })
    
    return render_template('teacher_grade_quiz.html', 
                         course=course, 
                         quiz=quiz, 
                         saq_data=saq_data)

@quiz_bp.route('/teacher/question/<int:question_id>/grade', methods=['POST'])
def teacher_grade_question(question_id):
    """Grade a specific question response"""
    # Check if user is logged in and is a teacher
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    
    user = User.query.get(user_id)
    if not user or user.role != 'teacher':
        return jsonify({'error': 'Not authorized'}), 403
    
    # Get question and verify teacher owns the course
    question = Question.query.get(question_id)
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    quiz = Quiz.query.get(question.quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    course = Course.query.get(quiz.course_code)
    if not course or course.teacher_id != user_id:
        return jsonify({'error': 'Not authorized for this course'}), 403
    
    # Get data from request
    data = request.get_json()
    if not data or 'submission_id' not in data or 'points' not in data:
        return jsonify({'error': 'Missing required data'}), 400
    
    submission_id = data['submission_id']
    points = float(data['points'])
    
    # Validate points
    if points < 0 or points > question.points:
        return jsonify({'error': f'Points must be between 0 and {question.points}'}), 400
    
    # Find the question response
    response = QuestionResponse.query.filter_by(
        submission_id=submission_id,
        question_id=question_id
    ).first()
    
    if not response:
        return jsonify({'error': 'Response not found'}), 404
    
    try:
        # Update the grade
        response.points = points
        response.is_correct = points == question.points
        db.session.commit()
        
        # Recalculate quiz grade for this submission
        submission = Submission.query.get(submission_id)
        if submission:
            calculate_and_save_quiz_grade(quiz.id, submission.user_id, submission.id)
        
        return jsonify({
            'success': True,
            'points': points,
            'max_points': question.points,
            'percentage': round((points / question.points) * 100, 1) if question.points > 0 else 0
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to save grade'}), 500