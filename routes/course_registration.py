from flask import Blueprint, render_template, redirect, url_for, flash
from functools import wraps

# Create blueprint for course registration routes
course_registration_bp = Blueprint('course_registration', __name__)

# Decorator to check if user is authenticated
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to check if user is a student
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import session
        from models.user import User
        from database import db
        
        # First check if user is logged in
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('auth.login'))
        
        # Get user role from database
        user = User.query.get(session['user_id'])
        if not user or user.role != 'student':
            flash('You need to be a student to access this page.')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

# Route for course registration page
@course_registration_bp.route('/course_registration')
@login_required
@student_required
def course_registration():
    # The actual course data will be loaded via JavaScript AJAX calls
    # This route just renders the template
    return render_template('course_registration.html')