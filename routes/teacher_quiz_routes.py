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
from routes.quiz_routes import calculate_and_save_quiz_grade

teacher_quiz_bp = Blueprint('teacher_quiz', __name__)

def teacher_required(f):
    """Decorator to check if user is logged in and is a teacher"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in to access this page.')
            return redirect(url_for('auth.login'))
        
        user = User.query.get(session['user_id'])
        if not user or user.role != 'teacher':
            flash('You need to be a teacher to access this page.')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

def check_teacher_course_access(course_code, user_id):
    """Check if teacher has access to the course"""
    course = Course.query.get(course_code)
    if not course:
        return None, "Course not found"
    
    if course.teacher_id != user_id:
        return None, "You are not the teacher of this course"
    
    return course, None

@teacher_quiz_bp.route('/teacher/course/<course_code>/quiz/<int:quiz_id>', methods=['GET'])
@teacher_required
def teacher_view_quiz(course_code, quiz_id):
    """Teacher view quiz - separate route from student view"""
    user_id = session.get('user_id')
    course, error = check_teacher_course_access(course_code, user_id)
    if error:
        return render_template('course_home.html', course=None, error_message=error), 404 if error == "Course not found" else 403
    
    # Get quiz details
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_info.html', course=course, quiz=None, quizzes=[], course_code=course_code, error_message="Quiz not found"), 404
    
    # Get all attempts for this quiz (teacher can see all student attempts)
    all_attempts = db.session.query(Attempt, User).join(
        User, Attempt.user_id == User.id
    ).filter(
        Attempt.quiz_id == quiz_id
    ).order_by(Attempt.attempt_count.desc()).all()
    
    # Get quiz statistics
    total_students = CourseEnrollment.query.filter_by(course_code=course_code).count()
    total_attempts = Attempt.query.filter_by(quiz_id=quiz_id).count()
    completed_submissions = Submission.query.filter_by(quiz_id=quiz_id).count()
    
    # Prepare quiz data for teacher view
    quiz_data = {
        'id': quiz.id,
        'name': quiz.name,
        'description': quiz.description,
        'duration': quiz.duration,
        'attempt_limit': quiz.attempt_limit,
        'start_datetime': quiz.start_datetime,
        'end_datetime': quiz.end_datetime,
        'total_students': total_students,
        'total_attempts': total_attempts,
        'completed_submissions': completed_submissions,
        'attempts': []
    }
    
    for attempt, user in all_attempts:
        # Get the latest submission for this user and quiz
        submission = Submission.query.filter_by(
            quiz_id=quiz_id, 
            user_id=user.id
        ).order_by(Submission.submitted_at.desc()).first()
        
        quiz_data['attempts'].append({
            'id': attempt.id,
            'student_name': user.username,
            'student_role': user.role,
            'attempt_count': attempt.attempt_count,
            'score': submission.grade if submission else None,
            'is_completed': submission is not None,
            'created_at': attempt.created_at
        })
    
    return render_template('teacher_quiz_info.html', course=course, quiz=quiz_data, course_code=course_code)

@teacher_quiz_bp.route('/teacher/course/<course_code>/quiz/<int:quiz_id>/start', methods=['GET'])
@teacher_required
def teacher_start_quiz(course_code, quiz_id):
    """Teacher start quiz - separate route from student start"""
    user_id = session.get('user_id')
    course, error = check_teacher_course_access(course_code, user_id)
    if error:
        return render_template('course_home.html', course=None, error_message=error), 404 if error == "Course not found" else 403
    
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
    
    # Get attempt count for teacher (teachers can attempt unlimited times)
    attempt_count = Attempt.query.filter_by(quiz_id=quiz_id, user_id=user_id).count()
    
    # Teachers can always attempt, regardless of availability or attempt limits
    # Get quiz questions
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Create new attempt for teacher
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
        'has_responded': False,  # Teachers don't have previous responses in teacher mode
        'used_attempts': attempt_count,
        'max_attempts': quiz.attempt_limit,
        'can_attempt': True,  # Teachers can always attempt
        'start_datetime': quiz.start_datetime,
        'end_datetime': quiz.end_datetime,
        'is_available': is_available,
        'questions': [{
            'id': q.id,
            'content': q.content,
            'type': q.type,
            'points': q.points,
            'choices': [{'id': c.id, 'content': c.content} for c in q.choices] if q.type == 'mcq' else []
        } for q in questions]
    }
    
    return render_template('teacher_quiz_start.html', course=course, quiz=quiz_data, course_code=course_code)

@teacher_quiz_bp.route('/teacher/course/<course_code>/quiz/<int:quiz_id>/submit', methods=['POST'])
@teacher_required
def teacher_submit_quiz(course_code, quiz_id):
    """Teacher submit quiz - separate route from student submit"""
    user_id = session.get('user_id')
    course, error = check_teacher_course_access(course_code, user_id)
    if error:
        return render_template('course_home.html', course=None, error_message=error), 404 if error == "Course not found" else 403
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_list.html', course=course, quizzes=[], error_message="Quiz not found", course_code=course_code), 404
    
    # Get current attempt ID from session
    attempt_id = session.get('current_attempt_id')
    if not attempt_id:
        return render_template('teacher_quiz_start.html', course=course, quiz=quiz, error_message="No active quiz attempt found", course_code=course_code), 400
    
    # Get the attempt
    attempt = Attempt.query.filter_by(id=attempt_id, user_id=user_id, quiz_id=quiz_id).first()
    if not attempt:
        return render_template('teacher_quiz_start.html', course=course, quiz=quiz, error_message="Invalid quiz attempt", course_code=course_code), 400
    
    # Get all questions for this quiz
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Process answers first to calculate scores
    total_points = 0
    all_answers_correct = True
    
    # Create submission record for teacher
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
    
    # Note: Attempt model doesn't have a score field, score is stored in submission.grade
    
    # Save all changes
    db.session.commit()
    
    # Calculate and save quiz grade
    success, message = calculate_and_save_quiz_grade(quiz_id, user_id, submission.id)
    if not success:
        print(f"Warning: {message}")
    
    # Clear the current attempt from session
    if 'current_attempt_id' in session:
        del session['current_attempt_id']
    
    # Redirect to teacher quiz results page
    return redirect(url_for('teacher_quiz.teacher_quiz_results', course_code=course_code, quiz_id=quiz_id))

@teacher_quiz_bp.route('/teacher/course/<course_code>/quiz/<int:quiz_id>/results', methods=['GET'])
@teacher_required
def teacher_quiz_results(course_code, quiz_id):
    """Teacher view quiz results - separate route from student results"""
    user_id = session.get('user_id')
    course, error = check_teacher_course_access(course_code, user_id)
    if error:
        return render_template('course_home.html', course=None, error_message=error), 404 if error == "Course not found" else 403
    
    # Get quiz
    quiz = Quiz.query.filter_by(id=quiz_id, course_code=course_code).first()
    if not quiz:
        return render_template('quiz_results.html', course=course, quiz=None, error_message="Quiz not found", course_code=course_code), 404
    
    # Get teacher's submissions for this quiz
    submissions = Submission.query.filter_by(quiz_id=quiz_id, user_id=user_id).order_by(Submission.submitted_at.desc()).all()
    
    if not submissions:
        return render_template('teacher_quiz_results.html', course=course, quiz=quiz, error_message="No submissions found for this quiz", course_code=course_code), 404
    
    # Get the most recent submission
    latest_submission = submissions[0]
    
    # Get all question responses for this submission
    responses = QuestionResponse.query.filter_by(submission_id=latest_submission.id).all()
    
    # Prepare results data
    results_data = {
        'id': quiz.id,
        'name': quiz.name,
        'description': quiz.description,
        'score': latest_submission.grade,
        'submitted_at': latest_submission.submitted_at,
        'total_submissions': len(submissions),
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
            'is_correct': response.is_correct,
            'correct_answer': None
        }
        
        if question.type == 'mcq':
            # Get the chosen answer
            if response.choice_id:
                choice = Choice.query.get(response.choice_id)
                if choice:
                    question_data['user_answer'] = choice.content
            
            # Get the correct answer
            correct_choice = Choice.query.filter_by(question_id=question.id, is_correct=True).first()
            if correct_choice:
                question_data['correct_answer'] = correct_choice.content
        
        elif question.type == 'saq':
            question_data['user_answer'] = response.text_answer
            # For SAQ, we might want to show a sample answer or leave it for manual grading
            question_data['correct_answer'] = "[Manual grading required]"
        
        results_data['questions'].append(question_data)
    
    return render_template('teacher_quiz_results.html', course=course, quiz=results_data, course_code=course_code)