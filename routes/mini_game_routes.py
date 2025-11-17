from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from functools import wraps
from models.course import Course
from models.minigame import Minigame, MinigameSession
from database import db
from datetime import datetime
from models.user import User

mini_game_bp = Blueprint('mini_game', __name__)

# Authentication decorator: Check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in to access this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Authentication decorator: Check if user is a teacher
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check if logged in
        if 'user_id' not in session:
            flash('You need to log in to access this page.')
            return redirect(url_for('auth.login'))
        
        # Get user role
        user = User.query.get(session['user_id'])
        if not user or user.role != 'teacher':
            flash('You need to be a teacher to access this page.')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

# Authentication decorator: Check if user is a student
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check if logged in
        if 'user_id' not in session:
            flash('You need to log in to access this page.')
            return redirect(url_for('auth.login'))
        
        # Get user role
        user = User.query.get(session['user_id'])
        if not user or user.role != 'student':
            flash('You need to be a student to access this page.')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

@mini_game_bp.route('/teacher/course/<course_code>/mini_games')
@login_required
@teacher_required
def teacher_mini_games_list(course_code):
    """Display all mini games for a teacher's course"""
    # Verify teacher owns the course
    course = Course.query.filter_by(code=course_code, teacher_id=session['user_id']).first()
    if not course:
        flash('Course not found or you do not have permission to access it.', 'error')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    # Get all mini games for this course
    mini_games = Minigame.query.filter_by(course_code=course_code).order_by(Minigame.created_at.desc()).all()
    
    return render_template('teacher_mini_games_list.html', 
                         course=course, 
                         mini_games=mini_games)

@mini_game_bp.route('/teacher/course/<course_code>/mini_games/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def teacher_create_mini_game(course_code):
    """Create a new mini game for a course"""
    # Verify teacher owns the course
    course = Course.query.filter_by(code=course_code, teacher_id=session['user_id']).first()
    if not course:
        flash('Course not found or you do not have permission to access it.', 'error')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        start_datetime_str = request.form.get('start_datetime')
        end_datetime_str = request.form.get('end_datetime')
        duration = request.form.get('duration', 30, type=int)
        attempt_limit = request.form.get('attempt_limit', 5, type=int)
        point = request.form.get('point', 100, type=int)
        point_in_course = request.form.get('point_in_course', 0, type=int)
        
        # Parse datetime strings
        start_datetime = None
        end_datetime = None
        if start_datetime_str:
            try:
                start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Invalid start datetime format.', 'error')
                return redirect(url_for('mini_game.teacher_create_mini_game', course_code=course_code))
        
        if end_datetime_str:
            try:
                end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Invalid end datetime format.', 'error')
                return redirect(url_for('mini_game.teacher_create_mini_game', course_code=course_code))
        
        # Validate dates
        if start_datetime and end_datetime and start_datetime >= end_datetime:
            flash('End datetime must be after start datetime.', 'error')
            return redirect(url_for('mini_game.teacher_create_mini_game', course_code=course_code))
        
        try:
            # Create new mini game
            mini_game = Minigame(
                course_code=course_code,
                name=name,
                description=description,
                created_by=session['user_id'],
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                duration=duration,
                attempt_limit=attempt_limit,
                point=point,
                point_in_course=point_in_course,
                config={}
            )
            
            db.session.add(mini_game)
            db.session.commit()
            
            flash('Mini game created successfully!', 'success')
            return redirect(url_for('mini_game.teacher_mini_games_list', course_code=course_code))
        except Exception as e:
            db.session.rollback()
            flash('Error creating mini game. Please try again.', 'error')
            return redirect(url_for('mini_game.teacher_create_mini_game', course_code=course_code))
    
    return render_template('teacher_create_mini_game.html', course=course)


# Student-side Mini Game Routes

@mini_game_bp.route('/course/<course_code>/mini_games')
@login_required
def student_mini_games_list(course_code):
    """Display all available mini games for a student's course"""
    # Verify student is enrolled in the course
    from models.course_enrollment import CourseEnrollment
    enrollment = CourseEnrollment.query.filter_by(
        student_id=session['user_id'], 
        course_code=course_code
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('course.student_course_home', course_code=course_code))
    
    # Get the course
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        flash('Course not found.', 'error')
        return redirect(url_for('student.student_home'))
    
    # Get all active mini games for this course
    from datetime import datetime
    now = datetime.now()
    mini_games = Minigame.query.filter_by(course_code=course_code).filter(
        (Minigame.start_datetime.is_(None)) | (Minigame.start_datetime <= now)
    ).filter(
        (Minigame.end_datetime.is_(None)) | (Minigame.end_datetime >= now)
    ).order_by(Minigame.created_at.desc()).all()
    
    # Get student's attempt counts for each mini game
    for game in mini_games:
        attempts = MinigameSession.query.filter_by(
            game_id=game.id,
            student_id=session['user_id']
        ).count()
        game.student_attempts = attempts
        game.can_attempt = attempts < game.attempt_limit
    
    return render_template('student_mini_games_list.html', 
                         course=course, 
                         mini_games=mini_games)

@mini_game_bp.route('/course/<course_code>/mini_games/<int:mini_game_id>')
@login_required
def student_mini_game_detail(course_code, mini_game_id):
    """Display details of a specific mini game for students"""
    # Verify student is enrolled in the course
    from models.course_enrollment import CourseEnrollment
    enrollment = CourseEnrollment.query.filter_by(
        student_id=session['user_id'], 
        course_code=course_code
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('course.student_course_home', course_code=course_code))
    
    # Get the course
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        flash('Course not found.', 'error')
        return redirect(url_for('student.student_home'))
    
    # Get the mini game
    mini_game = Minigame.query.filter_by(id=mini_game_id, course_code=course_code).first()
    if not mini_game:
        flash('Mini game not found.', 'error')
        return redirect(url_for('mini_game.student_mini_games_list', course_code=course_code))
    
    # Check if mini game is currently available
    from datetime import datetime
    now = datetime.now()
    if (mini_game.start_datetime and mini_game.start_datetime > now) or \
       (mini_game.end_datetime and mini_game.end_datetime < now):
        flash('This mini game is not currently available.', 'error')
        return redirect(url_for('mini_game.student_mini_games_list', course_code=course_code))
    
    # Get student's sessions for this mini game
    sessions = MinigameSession.query.filter_by(
        game_id=mini_game_id,
        student_id=session['user_id']
    ).order_by(MinigameSession.started_at.desc()).all()
    
    # Check if student can still attempt
    attempt_count = len(sessions)
    can_attempt = attempt_count < mini_game.attempt_limit
    
    return render_template('student_mini_game_detail.html', 
                         course=course, 
                         mini_game=mini_game,
                         sessions=sessions,
                         attempt_count=attempt_count,
                         can_attempt=can_attempt)

@mini_game_bp.route('/course/<course_code>/mini_games/<int:mini_game_id>/start', methods=['POST'])
@login_required
def student_start_mini_game(course_code, mini_game_id):
    """Start a new mini game session for a student"""
    # Verify student is enrolled in the course
    from models.course_enrollment import CourseEnrollment
    enrollment = CourseEnrollment.query.filter_by(
        student_id=session['user_id'], 
        course_code=course_code
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('course.student_course_home', course_code=course_code))
    
    # Get the mini game
    mini_game = Minigame.query.filter_by(id=mini_game_id, course_code=course_code).first()
    if not mini_game:
        flash('Mini game not found.', 'error')
        return redirect(url_for('mini_game.student_mini_games_list', course_code=course_code))
    
    # Check if mini game is currently available
    from datetime import datetime
    now = datetime.now()
    if (mini_game.start_datetime and mini_game.start_datetime > now) or \
       (mini_game.end_datetime and mini_game.end_datetime < now):
        flash('This mini game is not currently available.', 'error')
        return redirect(url_for('mini_game.student_mini_games_list', course_code=course_code))
    
    # Check attempt limit
    current_attempts = MinigameSession.query.filter_by(
        game_id=mini_game_id,
        student_id=session['user_id']
    ).count()
    
    if current_attempts >= mini_game.attempt_limit:
        flash('You have reached the maximum number of attempts for this mini game.', 'error')
        return redirect(url_for('mini_game.student_mini_game_detail', 
                              course_code=course_code, 
                              mini_game_id=mini_game_id))
    
    try:
        # Create new session
        session_obj = MinigameSession(
            game_id=mini_game_id,
            student_id=session['user_id'],
            started_at=now,
            score=0,
            is_completed=False
        )
        
        db.session.add(session_obj)
        db.session.commit()
        
        flash('Mini game started! Good luck!', 'success')
        return redirect(url_for('mini_game.student_mini_game_play', 
                              course_code=course_code, 
                              mini_game_id=mini_game_id,
                              session_id=session_obj.id))
        
    except Exception as e:
        db.session.rollback()
        flash('Error starting mini game. Please try again.', 'error')
        return redirect(url_for('mini_game.student_mini_game_detail', 
                              course_code=course_code, 
                              mini_game_id=mini_game_id))

@mini_game_bp.route('/course/<course_code>/mini_games/<int:mini_game_id>/play/<int:session_id>')
@login_required
def student_mini_game_play(course_code, mini_game_id, session_id):
    """Play a mini game (placeholder for actual game implementation)"""
    # Verify student is enrolled in the course
    from models.course_enrollment import CourseEnrollment
    enrollment = CourseEnrollment.query.filter_by(
        student_id=session['user_id'], 
        course_code=course_code
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('course.student_course_home', course_code=course_code))
    
    # Get the mini game
    mini_game = Minigame.query.filter_by(id=mini_game_id, course_code=course_code).first()
    if not mini_game:
        flash('Mini game not found.', 'error')
        return redirect(url_for('mini_game.student_mini_games_list', course_code=course_code))
    
    # Get the session
    session_obj = MinigameSession.query.filter_by(
        id=session_id,
        game_id=mini_game_id,
        student_id=session['user_id']
    ).first()
    
    if not session_obj:
        flash('Session not found.', 'error')
        return redirect(url_for('mini_game.student_mini_games_list', course_code=course_code))
    
    # Check if session is already completed
    if session_obj.is_completed:
        flash('This session has already been completed.', 'info')
        return redirect(url_for('mini_game.student_mini_game_detail', 
                              course_code=course_code, 
                              mini_game_id=mini_game_id))
    
    # This is a placeholder for the actual game implementation
    # For now, we'll just show a simple completion page
    return render_template('student_mini_game_play.html',
                         course=mini_game.course,
                         mini_game=mini_game,
                         session=session_obj)

@mini_game_bp.route('/course/<course_code>/mini_games/<int:mini_game_id>/complete/<int:session_id>', methods=['POST'])
@login_required
def student_complete_mini_game(course_code, mini_game_id, session_id):
    """Complete a mini game session (placeholder implementation)"""
    # Verify student is enrolled in the course
    from models.course_enrollment import CourseEnrollment
    enrollment = CourseEnrollment.query.filter_by(
        student_id=session['user_id'], 
        course_code=course_code
    ).first()
    
    if not enrollment:
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('course.student_course_home', course_code=course_code))
    
    # Get the session
    session_obj = MinigameSession.query.filter_by(
        id=session_id,
        game_id=mini_game_id,
        student_id=session['user_id']
    ).first()
    
    if not session_obj:
        flash('Session not found.', 'error')
        return redirect(url_for('mini_game.student_mini_games_list', course_code=course_code))
    
    if session_obj.is_completed:
        flash('This session has already been completed.', 'info')
        return redirect(url_for('mini_game.student_mini_game_detail', 
                              course_code=course_code, 
                              mini_game_id=mini_game_id))
    
    try:
        # Get score from form (placeholder - in real implementation, this would be calculated)
        score = request.form.get('score', 0, type=int)
        
        # Complete the session
        from datetime import datetime
        session_obj.score = score
        session_obj.is_completed = True
        session_obj.completed_at = datetime.now()
        
        db.session.commit()
        
        flash(f'Mini game completed! Your score: {score}', 'success')
        return redirect(url_for('mini_game.student_mini_game_detail', 
                              course_code=course_code, 
                              mini_game_id=mini_game_id))
        
    except Exception as e:
        db.session.rollback()
        flash('Error completing mini game. Please try again.', 'error')
        return redirect(url_for('mini_game.student_mini_game_play', 
                              course_code=course_code, 
                              mini_game_id=mini_game_id,
                              session_id=session_id))