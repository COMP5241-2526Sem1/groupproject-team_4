from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from models import db, WordCloud, WordEntry, User, Course, Submission
from datetime import datetime
from functools import wraps

word_cloud_bp = Blueprint('word_cloud', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

@word_cloud_bp.route('/course/<course_code>/word_cloud')
@login_required
def word_cloud_list(course_code):
    """Display all word clouds for a course"""
    user = get_current_user()
    course = Course.query.filter_by(code=course_code).first()
    
    if not course:
        return render_template('error.html', error_message="Course not found"), 404
    
    # Get all word clouds for this course
    word_clouds = WordCloud.query.filter_by(course_code=course_code).all()
    
    return render_template('word_cloud_list.html', 
                         course=course, 
                         word_clouds=word_clouds,
                         user=user)

@word_cloud_bp.route('/course/<course_code>/word_cloud/<int:word_cloud_id>')
@login_required
def word_cloud_detail(course_code, word_cloud_id):
    """Display a specific word cloud and allow word submission"""
    user = get_current_user()
    course = Course.query.filter_by(code=course_code).first()
    word_cloud = WordCloud.query.filter_by(id=word_cloud_id, course_code=course_code).first()
    
    if not course or not word_cloud:
        return render_template('error.html', error_message="Word cloud not found"), 404
    
    # Check if word cloud is currently available
    current_time = datetime.now()
    is_available = True
    if word_cloud.start_datetime and current_time < word_cloud.start_datetime:
        is_available = False
    if word_cloud.end_datetime and current_time > word_cloud.end_datetime:
        is_available = False
    
    return render_template('word_cloud_detail.html',
                         course=course,
                         word_cloud=word_cloud,
                         is_available=is_available,
                         user=user)

@word_cloud_bp.route('/api/word_cloud/<int:word_cloud_id>/data')
@login_required
def get_word_cloud_data(word_cloud_id):
    """API endpoint to get word cloud data for AJAX with HTTP caching"""
    word_cloud = WordCloud.query.filter_by(id=word_cloud_id).first()
    
    if not word_cloud:
        return jsonify({'error': 'Word cloud not found'}), 404
    
    # Get all word entries for this word cloud
    word_entries = WordEntry.query.filter_by(word_cloud_id=word_cloud_id).all()
    
    # Calculate word frequencies for visualization
    word_data = {}
    for entry in word_entries:
        if entry.word in word_data:
            word_data[entry.word] += entry.frequency
        else:
            word_data[entry.word] = entry.frequency
    
    # Find min and max frequencies for better scaling
    frequencies = list(word_data.values())
    min_freq = min(frequencies) if frequencies else 1
    max_freq = max(frequencies) if frequencies else 1
    
    # Convert to list format for easier frontend processing
    words_list = []
    for word, frequency in word_data.items():
        # Calculate size with better scaling - words with higher frequency appear much bigger
        # Scale from 14px (minimum) to 120px (maximum) based on relative frequency
        # This provides much more dramatic visual distinction for high-frequency words
        if max_freq > min_freq:
            relative_size = (frequency - min_freq) / (max_freq - min_freq)
            # Use exponential scaling for more dramatic difference
            exponential_scale = relative_size ** 0.7 if relative_size > 0 else 0
            font_size = 14 + (exponential_scale * 106)  # 14px to 120px range
        else:
            font_size = 20  # Default size when all frequencies are equal
        
        words_list.append({
            'text': word,
            'size': font_size,
            'frequency': frequency
        })
    
    # Create response data
    response_data = {
        'words': words_list,
        'total_words': len(word_data),
        'total_submissions': sum(word_data.values())
    }
    
    # Generate ETag based on data content
    import hashlib
    data_hash = hashlib.md5(str(response_data).encode()).hexdigest()
    etag = f'"{data_hash}"'
    
    # Check if client has matching ETag
    if_none_match = request.headers.get('If-None-Match')
    if if_none_match == etag:
        print(f"[CACHE HIT] Word cloud {word_cloud_id} - 304 Not Modified")
        return '', 304  # Not Modified
    
    print(f"[CACHE MISS] Word cloud {word_cloud_id} - Sending fresh data with ETag: {etag}")
    
    # Create response with ETag header
    response = jsonify(response_data)
    response.headers['ETag'] = etag
    response.headers['Cache-Control'] = 'no-cache'  # Still check with server but can use 304
    
    return response

@word_cloud_bp.route('/api/word_cloud/<int:word_cloud_id>/submit', methods=['POST'])
@login_required
def submit_word_cloud_ajax(word_cloud_id):
    """API endpoint for AJAX word cloud submission"""
    user = get_current_user()
    word_cloud = WordCloud.query.filter_by(id=word_cloud_id).first()
    
    if not word_cloud:
        return jsonify({'error': 'Word cloud not found'}), 404
    
    # Check if word cloud is currently available
    current_time = datetime.now()
    if word_cloud.start_datetime and current_time < word_cloud.start_datetime:
        return jsonify({'error': 'Word cloud not yet available'}), 400
    if word_cloud.end_datetime and current_time > word_cloud.end_datetime:
        return jsonify({'error': 'Word cloud has ended'}), 400
    
    # Allow multiple submissions - remove the restriction
    # existing_submission = Submission.query.filter_by(
    #     user_id=user.id, 
    #     word_cloud_id=word_cloud_id
    # ).first()
    
    # if existing_submission:
    #     return jsonify({'error': 'You have already submitted to this word cloud'}), 400
    
    # Get submitted words from JSON
    data = request.get_json()
    words = data.get('words', '').strip()
    
    if not words:
        return jsonify({'error': 'Please enter at least one word'}), 400
    
    # Process words (split by comma, space, or newline)
    word_list = [word.strip().lower() for word in words.replace(',', ' ').split() if word.strip()]
    
    if not word_list:
        return jsonify({'error': 'Please enter valid words'}), 400
    
    # Validate word length - database field is limited to 50 characters
    long_words = [word for word in word_list if len(word) > 50]
    if long_words:
        return jsonify({'error': f'Words cannot be longer than 50 characters. Please shorten: {", ".join(long_words)}'}), 400
    
    # Create word entries and update frequencies
    for word in word_list:
        # Check if word already exists for this user
        existing_entry = WordEntry.query.filter_by(
            word_cloud_id=word_cloud_id,
            word=word,
            submitted_by=user.id
        ).first()
        
        if existing_entry:
            existing_entry.frequency += 1
        else:
            new_entry = WordEntry(
                word_cloud_id=word_cloud_id,
                word=word,
                frequency=1,
                submitted_by=user.id
            )
            db.session.add(new_entry)
    
    # Create submission record for this submission instance
    submission = Submission(
        user_id=user.id,
        word_cloud_id=word_cloud_id,
        submitted_at=current_time,
        grade=word_cloud.point  # Award full points for participation
    )
    db.session.add(submission)
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Words submitted successfully!'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error submitting word cloud: {str(e)}'}), 500

# Teacher word cloud management routes
@word_cloud_bp.route('/teacher/course/<course_code>/word_cloud')
@login_required
def teacher_word_cloud_list(course_code):
    """Display teacher's word cloud management page"""
    user = get_current_user()
    
    if not user or user.role != 'teacher':
        return render_template('error.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        return render_template('error.html', error_message="Course not found"), 404
    
    if course.teacher_id != user.id:
        return render_template('error.html', error_message="You are not the teacher of this course"), 403
    
    # Get all word clouds for this course
    word_clouds = WordCloud.query.filter_by(course_code=course_code).all()
    
    return render_template('teacher_word_cloud_list.html', 
                         course=course, 
                         word_clouds=word_clouds,
                         user=user)

@word_cloud_bp.route('/teacher/course/<course_code>/word_cloud/create')
@login_required
def teacher_create_word_cloud(course_code):
    """Display create word cloud form"""
    user = get_current_user()
    
    if not user or user.role != 'teacher':
        return render_template('error.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        return render_template('error.html', error_message="Course not found"), 404
    
    if course.teacher_id != user.id:
        return render_template('error.html', error_message="You are not the teacher of this course"), 403
    
    return render_template('teacher_create_word_cloud.html', course=course, user=user)

@word_cloud_bp.route('/teacher/course/<course_code>/word_cloud/create', methods=['POST'])
@login_required
def teacher_save_word_cloud(course_code):
    """Save new word cloud"""
    user = get_current_user()
    
    if not user or user.role != 'teacher':
        return render_template('error.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        return render_template('error.html', error_message="Course not found"), 404
    
    if course.teacher_id != user.id:
        return render_template('error.html', error_message="You are not the teacher of this course"), 403
    
    # Get form data
    name = request.form.get('name')
    description = request.form.get('description')
    start_datetime = request.form.get('start_datetime')
    end_datetime = request.form.get('end_datetime')
    duration = request.form.get('duration', type=int)
    attempt_limit = request.form.get('attempt_limit', type=int)
    point = request.form.get('point', type=int)
    
    # Validate required fields
    if not name:
        flash('Name is required', 'error')
        return redirect(url_for('word_cloud.teacher_create_word_cloud', course_code=course_code))
    
    # Parse datetime if provided
    start_dt = None
    end_dt = None
    if start_datetime:
        try:
            start_dt = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid start datetime format', 'error')
            return redirect(url_for('word_cloud.teacher_create_word_cloud', course_code=course_code))
    
    if end_datetime:
        try:
            end_dt = datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid end datetime format', 'error')
            return redirect(url_for('word_cloud.teacher_create_word_cloud', course_code=course_code))
    
    # Create new word cloud
    word_cloud = WordCloud(
        course_code=course_code,
        name=name,
        description=description,
        created_by=user.id,
        created_at=datetime.now(),
        start_datetime=start_dt,
        end_datetime=end_dt,
        duration=duration or 0,
        attempt_limit=attempt_limit or 0,
        point=point or 0
    )
    
    db.session.add(word_cloud)
    
    try:
        db.session.commit()
        flash('Word cloud created successfully!', 'success')
        return redirect(url_for('word_cloud.teacher_word_cloud_list', course_code=course_code))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating word cloud: {str(e)}', 'error')
        return redirect(url_for('word_cloud.teacher_create_word_cloud', course_code=course_code))

@word_cloud_bp.route('/teacher/course/<course_code>/word_cloud/<int:word_cloud_id>/edit')
@login_required
def teacher_edit_word_cloud(course_code, word_cloud_id):
    """Display edit word cloud form"""
    user = get_current_user()
    
    if not user or user.role != 'teacher':
        return render_template('error.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        return render_template('error.html', error_message="Course not found"), 404
    
    if course.teacher_id != user.id:
        return render_template('error.html', error_message="You are not the teacher of this course"), 403
    
    # Get word cloud
    word_cloud = WordCloud.query.filter_by(id=word_cloud_id, course_code=course_code).first()
    if not word_cloud:
        return render_template('error.html', error_message="Word cloud not found"), 404
    
    return render_template('teacher_edit_word_cloud.html', course=course, word_cloud=word_cloud, user=user, now=datetime.now())

@word_cloud_bp.route('/teacher/course/<course_code>/word_cloud/<int:word_cloud_id>/edit', methods=['POST'])
@login_required
def teacher_update_word_cloud(course_code, word_cloud_id):
    """Update existing word cloud"""
    user = get_current_user()
    
    if not user or user.role != 'teacher':
        return render_template('error.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        return render_template('error.html', error_message="Course not found"), 404
    
    if course.teacher_id != user.id:
        return render_template('error.html', error_message="You are not the teacher of this course"), 403
    
    # Get word cloud
    word_cloud = WordCloud.query.filter_by(id=word_cloud_id, course_code=course_code).first()
    if not word_cloud:
        return render_template('error.html', error_message="Word cloud not found"), 404
    
    # Get form data
    name = request.form.get('name')
    description = request.form.get('description')
    start_datetime = request.form.get('start_datetime')
    end_datetime = request.form.get('end_datetime')
    duration = request.form.get('duration', type=int)
    attempt_limit = request.form.get('attempt_limit', type=int)
    point = request.form.get('point', type=int)
    
    # Validate required fields
    if not name:
        flash('Name is required', 'error')
        return redirect(url_for('word_cloud.teacher_edit_word_cloud', course_code=course_code, word_cloud_id=word_cloud_id))
    
    # Parse datetime if provided
    start_dt = None
    end_dt = None
    if start_datetime:
        try:
            start_dt = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid start datetime format', 'error')
            return redirect(url_for('word_cloud.teacher_edit_word_cloud', course_code=course_code, word_cloud_id=word_cloud_id))
    
    if end_datetime:
        try:
            end_dt = datetime.strptime(end_datetime, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid end datetime format', 'error')
            return redirect(url_for('word_cloud.teacher_edit_word_cloud', course_code=course_code, word_cloud_id=word_cloud_id))
    
    # Update word cloud
    word_cloud.name = name
    word_cloud.description = description
    word_cloud.start_datetime = start_dt
    word_cloud.end_datetime = end_dt
    word_cloud.duration = duration or 0
    word_cloud.attempt_limit = attempt_limit or 0
    word_cloud.point = point or 0
    
    try:
        db.session.commit()
        flash('Word cloud updated successfully!', 'success')
        return redirect(url_for('word_cloud.teacher_word_cloud_list', course_code=course_code))
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating word cloud: {str(e)}', 'error')
        return redirect(url_for('word_cloud.teacher_edit_word_cloud', course_code=course_code, word_cloud_id=word_cloud_id))

@word_cloud_bp.route('/teacher/course/<course_code>/word_cloud/<int:word_cloud_id>/delete', methods=['POST'])
@login_required
def teacher_delete_word_cloud(course_code, word_cloud_id):
    """Delete word cloud"""
    user = get_current_user()
    
    if not user or user.role != 'teacher':
        return render_template('error.html', error_message="You need to be a teacher to access this page"), 403
    
    # Verify course exists and teacher owns it
    course = Course.query.filter_by(code=course_code).first()
    if not course:
        return render_template('error.html', error_message="Course not found"), 404
    
    if course.teacher_id != user.id:
        return render_template('error.html', error_message="You are not the teacher of this course"), 403
    
    # Get word cloud
    word_cloud = WordCloud.query.filter_by(id=word_cloud_id, course_code=course_code).first()
    if not word_cloud:
        return render_template('error.html', error_message="Word cloud not found"), 404
    
    # Delete associated word entries and submissions first
    WordEntry.query.filter_by(word_cloud_id=word_cloud_id).delete()
    Submission.query.filter_by(word_cloud_id=word_cloud_id).delete()
    
    # Delete word cloud
    db.session.delete(word_cloud)
    
    try:
        db.session.commit()
        flash('Word cloud deleted successfully!', 'success')
        return redirect(url_for('word_cloud.teacher_word_cloud_list', course_code=course_code))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting word cloud: {str(e)}', 'error')
        return redirect(url_for('word_cloud.teacher_word_cloud_list', course_code=course_code))