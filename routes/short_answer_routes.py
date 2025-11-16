from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.short_answer import ShortAnswer
from models.question import Question
from models.choice import Choice
from models.course import Course
from models.submission import Submission
from models.question_response import QuestionResponse
from database import db
from datetime import datetime

short_answer_bp = Blueprint('short_answer', __name__)


@short_answer_bp.route('/teacher/course/<course_code>/short-answer')
def teacher_short_answer_list(course_code):
    """Display list of short answer activities for a course"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    course = Course.query.filter_by(code=course_code).first_or_404()
    short_answers = ShortAnswer.query.filter_by(course_code=course_code).all()
    
    return render_template('teacher_short_answer_list.html', 
                         course=course, 
                         short_answers=short_answers)


@short_answer_bp.route('/teacher/course/<course_code>/short-answer/create', methods=['GET', 'POST'])
def teacher_create_short_answer(course_code):
    """Create a new short answer activity"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    course = Course.query.filter_by(code=course_code).first_or_404()
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Create short answer activity
            short_answer = ShortAnswer(
                course_code=course_code,
                name=data.get('name'),
                description=data.get('description'),
                created_by=session['user_id'],
                duration=data.get('duration', 20),
                start_datetime=datetime.fromisoformat(data['start_datetime']) if data.get('start_datetime') else None,
                end_datetime=datetime.fromisoformat(data['end_datetime']) if data.get('end_datetime') else None,
                attempt_limit=data.get('attempt_limit', 5),
                point=data.get('point', 100),
                point_in_course=data.get('point_in_course', 0)
            )
            db.session.add(short_answer)
            db.session.flush()
            
            # Create questions
            for q_data in data.get('questions', []):
                question = Question(
                    short_answer_id=short_answer.id,
                    type='saq',
                    content=q_data.get('content'),
                    points=q_data.get('points', 5)
                )
                db.session.add(question)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'short_answer_id': short_answer.id,
                'redirect': url_for('short_answer.teacher_short_answer_list', course_code=course_code)
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('teacher_create_short_answer.html', course=course)


@short_answer_bp.route('/teacher/course/<course_code>/short-answer/<int:short_answer_id>/edit', methods=['GET', 'POST'])
def teacher_edit_short_answer(course_code, short_answer_id):
    """Edit a short answer activity"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    course = Course.query.filter_by(code=course_code).first_or_404()
    short_answer = ShortAnswer.query.get_or_404(short_answer_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Update short answer activity
            short_answer.name = data.get('name')
            short_answer.description = data.get('description')
            short_answer.duration = data.get('duration', 20)
            short_answer.start_datetime = datetime.fromisoformat(data['start_datetime']) if data.get('start_datetime') else None
            short_answer.end_datetime = datetime.fromisoformat(data['end_datetime']) if data.get('end_datetime') else None
            short_answer.attempt_limit = data.get('attempt_limit', 5)
            short_answer.point = data.get('point', 100)
            short_answer.point_in_course = data.get('point_in_course', 0)
            
            # Delete existing questions
            Question.query.filter_by(short_answer_id=short_answer.id).delete()
            
            # Create new questions
            for q_data in data.get('questions', []):
                question = Question(
                    short_answer_id=short_answer.id,
                    type='saq',
                    content=q_data.get('content'),
                    points=q_data.get('points', 5)
                )
                db.session.add(question)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'redirect': url_for('short_answer.teacher_short_answer_list', course_code=course_code)
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('teacher_edit_short_answer.html', 
                         course=course, 
                         short_answer=short_answer)


@short_answer_bp.route('/teacher/course/<course_code>/short-answer/<int:short_answer_id>/delete', methods=['POST'])
def teacher_delete_short_answer(course_code, short_answer_id):
    """Delete a short answer activity"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        short_answer = ShortAnswer.query.get_or_404(short_answer_id)
        db.session.delete(short_answer)
        db.session.commit()
        
        flash('Short answer activity deleted successfully', 'success')
        return redirect(url_for('short_answer.teacher_short_answer_list', course_code=course_code))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting short answer activity: {str(e)}', 'error')
        return redirect(url_for('short_answer.teacher_short_answer_list', course_code=course_code))


@short_answer_bp.route('/course/<course_code>/short-answer/<int:short_answer_id>')
def short_answer_detail(course_code, short_answer_id):
    """View short answer activity details (for students)"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    course = Course.query.filter_by(code=course_code).first_or_404()
    short_answer = ShortAnswer.query.get_or_404(short_answer_id)
    
    # Get student's submissions
    submissions = Submission.query.filter_by(
        user_id=session['user_id'],
        short_answer_id=short_answer_id
    ).all()
    
    return render_template('short_answer_detail.html',
                         course=course,
                         short_answer=short_answer,
                         submissions=submissions)


@short_answer_bp.route('/course/<course_code>/short-answer/<int:short_answer_id>/start', methods=['GET', 'POST'])
def short_answer_start(course_code, short_answer_id):
    """Start a short answer activity"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    course = Course.query.filter_by(code=course_code).first_or_404()
    short_answer = ShortAnswer.query.get_or_404(short_answer_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Create submission
            submission = Submission(
                user_id=session['user_id'],
                short_answer_id=short_answer_id,
                submitted_at=datetime.now()
            )
            db.session.add(submission)
            db.session.flush()
            
            # Save answers
            total_points = 0
            for answer in data.get('answers', []):
                question = Question.query.get(answer['question_id'])
                
                response = QuestionResponse(
                    submission_id=submission.id,
                    question_id=answer['question_id'],
                    text_answer=answer.get('text_answer'),
                    points=0  # Will be graded by teacher
                )
                db.session.add(response)
            
            submission.total_score = 0  # Will be graded later
            db.session.commit()
            
            return jsonify({
                'success': True,
                'submission_id': submission.id,
                'redirect': url_for('short_answer.short_answer_detail', 
                                  course_code=course_code, 
                                  short_answer_id=short_answer_id)
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)}), 500
    
    return render_template('short_answer_start.html',
                         course=course,
                         short_answer=short_answer)


@short_answer_bp.route('/teacher/course/<course_code>/short-answer/<int:short_answer_id>/grade')
def teacher_grade_short_answer(course_code, short_answer_id):
    """Teacher grading page for short answer activities"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    course = Course.query.filter_by(code=course_code).first_or_404()
    short_answer = ShortAnswer.query.get_or_404(short_answer_id)
    
    # Get all submissions
    submissions = Submission.query.filter_by(short_answer_id=short_answer_id).all()
    
    # Organize by question
    questions_data = []
    for question in short_answer.questions:
        responses = QuestionResponse.query.filter_by(question_id=question.id).all()
        questions_data.append({
            'question': question,
            'responses': responses
        })
    
    return render_template('teacher_grade_short_answer.html',
                         course=course,
                         short_answer=short_answer,
                         submissions=submissions,
                         questions_data=questions_data)


@short_answer_bp.route('/api/short-answer/grade', methods=['POST'])
def grade_response():
    """Grade a short answer response"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    try:
        data = request.get_json()
        response_id = data.get('response_id')
        points = data.get('points')
        
        response = QuestionResponse.query.get_or_404(response_id)
        response.points = points
        response.is_correct = (points > 0)
        
        # Update submission total score
        submission = Submission.query.get(response.submission_id)
        total = db.session.query(db.func.sum(QuestionResponse.points)).filter_by(
            submission_id=submission.id
        ).scalar() or 0
        submission.total_score = total
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
