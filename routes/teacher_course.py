from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from functools import wraps
from database import db
from models.user import User
from models.course import Course
from models.course_enrollment import CourseEnrollment
import csv
import io
import random
import string

# Create teacher course management blueprint
teacher_course_bp = Blueprint('teacher_course', __name__)

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

# Generate random course code
def generate_course_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Teacher course homepage - Display all courses
@teacher_course_bp.route('/teacher_course_list')
@login_required
@teacher_required
def teacher_course_list():
    # Get current teacher ID
    teacher_id = session['user_id']
    
    # Get courses created by the teacher
    my_courses = Course.query.filter_by(teacher_id=teacher_id).all()
    
    # Get courses created by other teachers
    other_courses = Course.query.filter(Course.teacher_id != teacher_id).all()
    
    return render_template('teacher_course_list.html', my_courses=my_courses, other_courses=other_courses)

# API endpoint for teacher course list (for dropdown menu)
@teacher_course_bp.route('/teacher_course_list/list')
@login_required
@teacher_required
def get_teacher_courses():
    # Get current teacher ID
    teacher_id = session['user_id']
    
    # Get courses created by the teacher
    courses = Course.query.filter_by(teacher_id=teacher_id).all()
    
    # Return course list in JSON format
    course_list = [{
        'code': course.code,
        'name': course.name
    } for course in courses]
    
    return jsonify(course_list)

# Teacher course detail page
@teacher_course_bp.route('/teacher_course/<course_code>')
@login_required
@teacher_required
def teacher_course_detail(course_code):
    # Get course information
    course = Course.query.get_or_404(course_code)
    
    # Check if the user is the teacher of this course
    if course.teacher_id != session['user_id']:
        flash('You are not the teacher of this course, cannot access this page.')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    # Get the number of students enrolled in the course
    enrolled_count = CourseEnrollment.query.filter_by(course_code=course_code).count()
    
    return render_template('teacher_course_detail.html', course=course, enrolled_count=enrolled_count)

# Create new course page
@teacher_course_bp.route('/teacher_course/create', methods=['GET', 'POST'])
@login_required
@teacher_required
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
        
        # If department_code is provided, use it; otherwise try to extract from course code format
        final_department_code = department_code if department_code else None
        final_course_number = None
        
        # If course name follows department format (e.g., COMP1010), extract components
        import re
        dept_pattern = re.match(r'^([A-Za-z]+)(\d+)$', name.replace(" ", ""))
        if dept_pattern:
            final_department_code = dept_pattern.group(1).upper()
            final_course_number = dept_pattern.group(2)
        
        # Generate unique course code if not provided in format
        if not final_department_code or not final_course_number:
            code = generate_course_code()
            while Course.query.filter_by(code=code).first():
                code = generate_course_code()
            # Try to extract department from name or use default
            if not final_department_code:
                name_pattern = re.match(r'^([A-Za-z]+)', name)
                final_department_code = name_pattern.group(1).upper() if name_pattern else 'DEPT'
            if not final_course_number:
                final_course_number = code[:4]  # Use part of generated code
        else:
            # Use the extracted format
            code = final_department_code + final_course_number
            # Ensure uniqueness
            counter = 1
            original_code = code
            while Course.query.filter_by(code=code).first():
                code = f"{original_code}_{counter}"
                counter += 1
        
        # Create new course
        new_course = Course(
            code=code,
            name=name,
            description=description,
            teacher_id=session['user_id'],
            credit=credit,
            capacity=capacity,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            department_code=final_department_code,
            course_number=final_course_number
        )
        
        # Save to database
        db.session.add(new_course)
        db.session.commit()
        
        flash('Course created successfully!')
        return redirect(url_for('teacher_course.teacher_course_detail', course_code=new_course.code))
    
    return render_template('create_course.html')

# Enrolled students list page
@teacher_course_bp.route('/teacher_course/<course_code>/enrolled_list', methods=['GET', 'POST'])
@login_required
@teacher_required
def enrolled_list(course_code):
    # Get course information
    course = Course.query.get_or_404(course_code)
    
    # Check if the user is the teacher of this course
    if course.teacher_id != session['user_id']:
        flash('You are not the teacher of this course, cannot access this page.')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    # Get search criteria
    department_filter = request.args.get('department')
    
    # Get enrolled students
    enrolled_students = db.session.query(User).join(
        CourseEnrollment, User.id == CourseEnrollment.student_id
    ).filter(
        CourseEnrollment.course_code == course_code
    )
    
    # Apply department filter
    if department_filter:
        enrolled_students = enrolled_students.filter(User.department == department_filter)
    
    enrolled_students = enrolled_students.all()
    
    # Handle removing students
    if request.method == 'POST':
        student_ids = request.form.getlist('students[]')
        if student_ids:
            try:
                # Delete selected student enrollment records
                deleted_count = CourseEnrollment.query.filter(
                    CourseEnrollment.course_code == course_code,
                    CourseEnrollment.student_id.in_(student_ids)
                ).delete(synchronize_session=False)
                db.session.commit()
                if deleted_count > 0:
                    flash(f'Successfully removed {deleted_count} students from the course.', 'success')
                else:
                    flash('No students were removed.', 'warning')
            except Exception as e:
                db.session.rollback()
                flash(f'Error removing students: {str(e)}', 'error')
        return redirect(url_for('teacher_course.enrolled_list', course_code=course_code))
    
    return render_template('enrolled_list.html', course=course, students=enrolled_students)

# Not enrolled students list page
@teacher_course_bp.route('/teacher_course/<course_code>/not_enrolled_list', methods=['GET', 'POST'])
@login_required
@teacher_required
def not_enrolled_list(course_code):
    course = Course.query.get_or_404(course_code)
    
    # Check if the teacher owns this course
    if course.teacher_id != session['user_id']:
        flash('You can only manage students in your own courses.', 'error')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    if request.method == 'POST':
        student_ids = request.form.getlist('students[]')
        if student_ids:
            try:
                # Check course capacity
                enrolled_count = CourseEnrollment.query.filter_by(course_code=course_code).count()
                available_slots = course.capacity - enrolled_count
                
                if available_slots <= 0:
                    flash('Course is at full capacity. No students can be added.', 'warning')
                    return redirect(url_for('teacher_course.not_enrolled_list', course_code=course_code))
                
                # Only add students up to available capacity
                students_to_add = min(len(student_ids), available_slots)
                added_count = 0
                
                for i in range(students_to_add):
                    student_id = student_ids[i]
                    # Check if student is already enrolled
                    existing = CourseEnrollment.query.filter_by(
                        course_code=course_code, 
                        student_id=student_id
                    ).first()
                    
                    if not existing:
                        enrollment = CourseEnrollment(
                            course_code=course_code,
                            student_id=student_id
                        )
                        db.session.add(enrollment)
                        added_count += 1
                
                if added_count > 0:
                    db.session.commit()
                    flash(f'Successfully added {added_count} student(s) to the course.', 'success')
                    if students_to_add < len(student_ids):
                        flash(f'Course capacity reached. {len(student_ids) - students_to_add} student(s) could not be added.', 'warning')
                else:
                    flash('No students were added (they may already be enrolled).', 'warning')
                    
            except Exception as e:
                db.session.rollback()
                flash(f'Error adding students: {str(e)}', 'error')
                
        return redirect(url_for('teacher_course.not_enrolled_list', course_code=course_code))
    
    # Get not enrolled students with department filtering
    department = request.args.get('department', '')
    query = User.query.filter(User.role == 'student')
    
    if department:
        query = query.filter(User.department == department)
    
    # Exclude already enrolled students
    enrolled_student_ids = db.session.query(CourseEnrollment.student_id).filter(
        CourseEnrollment.course_code == course_code
    ).subquery()
    
    not_enrolled_students = query.filter(~User.id.in_(enrolled_student_ids)).all()
    
    return render_template('not_enrolled_list.html', course=course, students=not_enrolled_students)

# CSV import students page
@teacher_course_bp.route('/teacher_course/<course_code>/import_students', methods=['GET', 'POST'])
@login_required
@teacher_required
def import_students(course_code):
    course = Course.query.get_or_404(course_code)
    
    # Check if the user is the teacher of this course
    if course.teacher_id != session['user_id']:
        flash('You can only manage students in your own courses.', 'error')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file uploaded.', 'error')
            return redirect(request.url)
        
        file = request.files['csv_file']
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            try:
                csv_content = file.read().decode('utf-8')
                csv_reader = csv.DictReader(csv_content.splitlines())
                
                added_count = 0
                skipped_count = 0
                invalid_rows = 0
                
                # Check current capacity
                enrolled_count = CourseEnrollment.query.filter_by(course_code=course_code).count()
                available_slots = course.capacity - enrolled_count
                
                for row_num, row in enumerate(csv_reader, start=2):
                    try:
                        student_id = row.get('student_id', '').strip()
                        email = row.get('email', '').strip()
                        
                        # Validate row data
                        if not student_id and not email:
                            invalid_rows += 1
                            continue
                        
                        # Find student by ID or email
                        student = None
                        if student_id:
                            try:
                                student_id_int = int(student_id)
                                student = User.query.filter_by(id=student_id_int, role='student').first()
                            except ValueError:
                                invalid_rows += 1
                                continue
                        elif email:
                            student = User.query.filter_by(email=email, role='student').first()
                        
                        if student:
                            # Check if already enrolled
                            existing = CourseEnrollment.query.filter_by(
                                course_code=course_code,
                                student_id=student.id
                            ).first()
                            
                            if not existing and available_slots > 0:
                                enrollment = CourseEnrollment(
                                    course_code=course_code,
                                    student_id=student.id
                                )
                                db.session.add(enrollment)
                                added_count += 1
                                available_slots -= 1
                            else:
                                skipped_count += 1
                        else:
                            skipped_count += 1
                            
                    except Exception as e:
                        invalid_rows += 1
                        continue
                
                if added_count > 0:
                    db.session.commit()
                    flash(f'CSV import completed successfully. Added {added_count} students.', 'success')
                else:
                    flash('No students were added from the CSV file.', 'warning')
                
                # Provide detailed feedback
                messages = []
                if skipped_count > 0:
                    messages.append(f'{skipped_count} skipped (already enrolled or not found)')
                if invalid_rows > 0:
                    messages.append(f'{invalid_rows} invalid rows')
                if available_slots <= 0 and added_count == 0:
                    messages.append('Course is at full capacity')
                
                if messages:
                    flash('Details: ' + ', '.join(messages), 'info')
                
            except UnicodeDecodeError:
                flash('Error reading CSV file. Please ensure it\'s properly encoded (UTF-8).', 'error')
            except csv.Error as e:
                flash(f'CSV format error: {str(e)}', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error processing CSV file: {str(e)}', 'error')
        else:
            flash('Please upload a valid CSV file (.csv extension required).', 'error')
    
    return render_template('import_students.html', course=course)


@teacher_course_bp.route('/teacher_course/<course_code>/bulk_remove', methods=['POST'])
@login_required
@teacher_required
def bulk_remove_students(course_code):
    course = Course.query.get_or_404(course_code)
    
    # Check if the teacher owns this course
    if course.teacher_id != current_user.id:
        flash('You can only manage students in your own courses.', 'error')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    student_ids = request.form.getlist('student_ids[]')
    
    if not student_ids:
        flash('No students selected for removal.', 'warning')
        return redirect(url_for('teacher_course.enrolled_list', course_code=course_code))
    
    try:
        removed_count = 0
        
        for student_id in student_ids:
            enrollment = CourseEnrollment.query.filter_by(
                course_code=course.code,
                student_id=student_id
            ).first()
            
            if enrollment:
                db.session.delete(enrollment)
                removed_count += 1
        
        if removed_count > 0:
            db.session.commit()
            flash(f'Successfully removed {removed_count} students from the course.', 'success')
        else:
            flash('No students were removed (none found in course).', 'warning')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error removing students: {str(e)}', 'error')
    
    return redirect(url_for('teacher_course.enrolled_list', course_code=course_code))


@teacher_course_bp.route('/teacher_course/<course_code>/bulk_add', methods=['POST'])
@login_required
@teacher_required
def bulk_add_students(course_code):
    course = Course.query.get_or_404(course_code)
    
    # Check if the teacher owns this course
    if course.teacher_id != current_user.id:
        flash('You can only manage students in your own courses.', 'error')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    student_ids = request.form.getlist('student_ids[]')
    
    if not student_ids:
        flash('No students selected for addition.', 'warning')
        return redirect(url_for('teacher_course.not_enrolled_list', course_code=course_code))
    
    try:
        # Check current capacity
        enrolled_count = CourseEnrollment.query.filter_by(course_code=course.code).count()
        available_slots = course.capacity - enrolled_count
        
        if available_slots <= 0:
            flash('Course is at full capacity. No students can be added.', 'error')
            return redirect(url_for('teacher_course.not_enrolled_list', course_code=course_code))
        
        added_count = 0
        
        for student_id in student_ids:
            # Check if already enrolled
            existing = CourseEnrollment.query.filter_by(
                course_code=course.code,
                student_id=student_id
            ).first()
            
            if not existing and available_slots > 0:
                enrollment = CourseEnrollment(
                    course_code=course.code,
                    student_id=student_id
                )
                db.session.add(enrollment)
                added_count += 1
                available_slots -= 1
        
        if added_count > 0:
            db.session.commit()
            flash(f'Successfully added {added_count} students to the course.', 'success')
            
            if available_slots <= 0 and len(student_ids) > added_count:
                flash('Course capacity reached. Some students were not added.', 'warning')
        else:
            flash('No students were added (all already enrolled).', 'warning')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding students: {str(e)}', 'error')
    
    return redirect(url_for('teacher_course.not_enrolled_list', course_code=course_code))