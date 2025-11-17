from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from functools import wraps
from database import db
from models.user import User
from models.course import Course
from models.course_enrollment import CourseEnrollment
from models.minigame import Minigame
import csv
import io
import random
import string

# Create admin course management blueprint
admin_course_bp = Blueprint('admin_course', __name__)

# Authentication decorator: Check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You need to log in to access this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Authentication decorator: Check if user is an admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # First check if logged in
        if 'user_id' not in session:
            flash('You need to log in to access this page.')
            return redirect(url_for('auth.login'))
        
        # Get user role
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            flash('You need to be an admin to access this page.')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

# Generate random course code
def generate_course_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Admin course homepage - Display all courses
@admin_course_bp.route('/admin/course_list')
@login_required
@admin_required
def admin_course_list():
    # Get filter parameters from request
    search = request.args.get('search', '').strip()
    department = request.args.get('department', '').strip()
    
    # Build query with filters
    query = Course.query
    
    # Apply search filter (search in course name or code)
    if search:
        query = query.filter(
            db.or_(
                Course.name.ilike(f'%{search}%'),
                Course.code.ilike(f'%{search}%')
            )
        )
    
    # Apply department filter
    if department:
        query = query.filter(Course.department_code == department)
    
    # Execute query and get results
    courses = query.all()
    
    return render_template('admin_course_list.html', courses=courses)

# API endpoint for admin course list (for dropdown menu)
@admin_course_bp.route('/admin/course_list/list')
@login_required
@admin_required
def get_admin_courses():
    # Get all courses for admin
    courses = Course.query.all()
    
    # Return course list in JSON format
    course_list = [{
        'code': course.code,
        'name': course.name
    } for course in courses]
    
    return jsonify(course_list)

# Admin course detail page
@admin_course_bp.route('/admin/course/<course_code>')
@login_required
@admin_required
def admin_course_detail(course_code):
    # Get course information
    course = Course.query.get_or_404(course_code)
    
    # Get the number of students enrolled in the course
    enrolled_count = CourseEnrollment.query.filter_by(course_code=course_code).count()
    
    return render_template('admin_course_home.html', course=course, enrolled_count=enrolled_count)

# Admin course dashboard page
@admin_course_bp.route('/admin/course/<course_code>/dashboard')
@login_required
@admin_required
def admin_course_dashboard(course_code):
    # Get course information
    course = Course.query.get_or_404(course_code)
    
    # Get enrolled students with their participation data
    from models.course_enrollment import CourseEnrollment
    from sqlalchemy import func
    
    # Get student participation data
    enrolled_students = db.session.query(
        User,
        func.count(CourseEnrollment.id).label('activities_completed')
    ).join(
        CourseEnrollment, User.id == CourseEnrollment.student_id
    ).filter(
        CourseEnrollment.course_code == course_code
    ).group_by(User.id).all()
    
    # Calculate total activities for this course
    from models.quiz import Quiz
    from models.poll import Poll
    from models.word_cloud import WordCloud
    
    total_quizzes = Quiz.query.filter_by(course_code=course_code).count()
    total_polls = Poll.query.filter_by(course_code=course_code).count()
    total_word_clouds = WordCloud.query.filter_by(course_code=course_code).count()
    total_mini_games = Minigame.query.filter_by(course_code=course_code).count()
    
    total_activities = total_quizzes + total_polls + total_word_clouds + total_mini_games
    
    # Create student ranking data
    student_rankings = []
    for student, activities_completed in enrolled_students:
        participation_rate = (activities_completed / total_activities * 100) if total_activities > 0 else 0
        student_rankings.append({
            'student': student,
            'activities_completed': activities_completed,
            'participation_rate': participation_rate
        })
    
    # Sort by participation rate (descending)
    student_rankings.sort(key=lambda x: x['participation_rate'], reverse=True)
    
    # Get enrolled count
    enrolled_count = CourseEnrollment.query.filter_by(course_code=course_code).count()
    
    return render_template('admin_course_dashboard.html', 
                         course=course, 
                         student_rankings=student_rankings,
                         total_activities=total_activities,
                         enrolled_count=enrolled_count)

# Create new course page
@admin_course_bp.route('/admin/course/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_course():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        description = request.form['description']
        credit = int(request.form['credit'])
        capacity = int(request.form['capacity'])
        day_of_week = request.form['day_of_week']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        department_code = request.form.get('department_code')  # Optional field
        teacher_id = request.form.get('teacher_id')  # Admin can assign teacher
        
        # If department_code is provided, use it; otherwise try to extract from course code format
        import re
        dept_pattern = re.match(r'^([A-Za-z]+)(\d+)$', name.replace(" ", ""))
        if dept_pattern:
            final_department_code = dept_pattern.group(1).upper()
            final_course_number = dept_pattern.group(2)
        else:
            final_department_code = department_code if department_code else 'DEPT'
            final_course_number = None
        
        # Generate unique course code if not provided in format
        code = generate_course_code()
        while Course.query.filter_by(code=code).first():
            code = generate_course_code()
        
        # Create new course
        new_course = Course(
            code=code,
            name=name,
            description=description,
            credit=credit,
            capacity=capacity,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            department_code=final_department_code,
            teacher_id=teacher_id if teacher_id else session['user_id']
        )
        
        try:
            db.session.add(new_course)
            db.session.commit()
            flash('Course created successfully!')
            return redirect(url_for('admin_course.admin_course_detail', course_code=code))
        except Exception as e:
            db.session.rollback()
            flash('Failed to create course: ' + str(e))
            return redirect(url_for('admin_course.create_course'))
    
    # Get all teachers for dropdown
    teachers = User.query.filter_by(role='teacher').all()
    
    return render_template('create_course.html', teachers=teachers)

# Admin manage students page
@admin_course_bp.route('/admin/course/<course_code>/enrolled_list')
@login_required
@admin_required
def admin_enrolled_list(course_code):
    # Get course information
    course = Course.query.get_or_404(course_code)
    
    # Get all enrolled students
    enrolled_students = CourseEnrollment.query.filter_by(course_code=course_code).all()
    
    return render_template('admin_enrolled_list.html', course=course, enrolled_students=enrolled_students)

# Admin manage all users
@admin_course_bp.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Admin user management page"""
    try:
        # Get filter parameters
        search = request.args.get('search', '')
        role = request.args.get('role', '')
        
        # Build query
        query = User.query
        if search:
            query = query.filter(User.username.contains(search) | User.email.contains(search))
        if role:
            query = query.filter_by(role=role)
        
        users = query.all()
        return render_template('admin_users.html', users=users)
    except Exception as e:
        current_app.logger.error(f"Error in admin user_management: {e}")
        flash('Error loading users', 'error')
        return redirect(url_for('admin_course.admin_dashboard'))

# Admin dashboard
@admin_course_bp.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    # Get statistics
    total_courses = Course.query.count()
    total_users = User.query.count()
    total_teachers = User.query.filter_by(role='teacher').count()
    total_students = User.query.filter_by(role='student').count()
    
    # Get recent courses
    recent_courses = Course.query.order_by(Course.code.desc()).limit(5).all()
    
    return render_template('admin_dashboard.html', 
                         total_courses=total_courses,
                         total_users=total_users,
                         total_teachers=total_teachers,
                         total_students=total_students,
                         recent_courses=recent_courses)