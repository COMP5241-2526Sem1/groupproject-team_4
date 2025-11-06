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
        'id': course.id,
        'name': course.name,
        'code': course.code
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
            # Delete selected student enrollment records
            CourseEnrollment.query.filter(
                CourseEnrollment.course_code == course_code,
                CourseEnrollment.student_id.in_(student_ids)
            ).delete(synchronize_session=False)
            db.session.commit()
            flash(f'Successfully removed {len(student_ids)} students from the course.')
        return redirect(url_for('teacher_course.enrolled_list', course_code=course_code))
    
    return render_template('enrolled_list.html', course=course, students=enrolled_students)

# Not enrolled students list page
@teacher_course_bp.route('/teacher_course/<course_code>/not_enrolled_list', methods=['GET', 'POST'])
@login_required
@teacher_required
def not_enrolled_list(course_code):
    # Get course information
    course = Course.query.get_or_404(course_code)
    
    # Check if the user is the teacher of this course
    if course.teacher_id != session['user_id']:
        flash('You are not the teacher of this course, cannot access this page.')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    # Get search criteria
    department_filter = request.args.get('department')
    
    # Get not enrolled students
    not_enrolled_students = User.query.filter(
        User.role == 'student',
        User.id.notin_(
            db.session.query(CourseEnrollment.student_id)
            .filter(CourseEnrollment.course_code == course_code)
        )
    )
    
    # Apply department filter
    if department_filter:
        not_enrolled_students = not_enrolled_students.filter(User.department == department_filter)
    
    not_enrolled_students = not_enrolled_students.all()
    
    # Handle adding students
    if request.method == 'POST':
        student_ids = request.form.getlist('students[]')
        if student_ids:
            # Check course capacity
            current_enrolled = CourseEnrollment.query.filter_by(course_code=course_code).count()
            if current_enrolled + len(student_ids) > course.capacity:
                flash('The number of students to add exceeds the course capacity limit.')
                return redirect(url_for('teacher_course.not_enrolled_list', course_code=course_code))
            
            # Add selected students
            for student_id in student_ids:
                enrollment = CourseEnrollment(
                    course_code=course_code,
                    student_id=student_id
                )
                db.session.add(enrollment)
            db.session.commit()
            flash(f'Successfully added {len(student_ids)} students to the course.')
        return redirect(url_for('teacher_course.not_enrolled_list', course_code=course_code))
    
    return render_template('not_enrolled_list.html', course=course, students=not_enrolled_students)

# CSV import students page
@teacher_course_bp.route('/teacher_course/<course_code>/import_students', methods=['GET', 'POST'])
@login_required
@teacher_required
def import_students(course_code):
    # Get course information
    course = Course.query.get_or_404(course_code)
    
    # Check if the user is the teacher of this course
    if course.teacher_id != session['user_id']:
        flash('You are not the teacher of this course, cannot access this page.')
        return redirect(url_for('teacher_course.teacher_course_list'))
    
    # Handle CSV file upload
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'csv_file' not in request.files or request.files['csv_file'].filename == '':
            flash('Please select a CSV file to upload.')
            return redirect(request.url)
        
        csv_file = request.files['csv_file']
        
        # Check file type
        if not csv_file.filename.endswith('.csv'):
            flash('Please upload a CSV format file.')
            return redirect(request.url)
        
        # Parse CSV file
        csv_data = []
        try:
            # Read CSV file content
            stream = io.StringIO(csv_file.stream.read().decode('utf-8'))
            reader = csv.DictReader(stream)
            
            # Check if CSV format is correct
            required_columns = ['student_id', 'email']  # At least student_id or email is required
            if not any(col in reader.fieldnames for col in required_columns):
                flash('CSV file format is incorrect, must contain at least student_id or email column.')
                return redirect(request.url)
            
            csv_data = list(reader)
        except Exception as e:
            flash(f'Error parsing CSV file: {str(e)}')
            return redirect(request.url)
        
        # Process student data
        enrolled_students = []
        not_enrolled_students = []
        errors = []
        
        for row in csv_data:
            student = None
            
            # Try to find by student ID
            if 'student_id' in row and row['student_id']:
                # Convert student_id to integer type
                try:
                    student_id = int(row['student_id'])
                    student = User.query.filter_by(id=student_id, role='student').first()
                except ValueError:
                    # If conversion fails, continue trying to find by email
                    student = None
            
            # If not found, try to find by email
            if not student and 'email' in row and row['email']:
                student = User.query.filter_by(email=row['email'], role='student').first()
            
            if not student:
                errors.append(f"Student not found: {row}")
                continue
            
            # Check if student is already enrolled in the course
            enrollment = CourseEnrollment.query.filter_by(
                course_code=course_code,
                student_id=student.id
            ).first()
            
            if enrollment:
                enrolled_students.append(student)
            else:
                not_enrolled_students.append(student)
        
        # If there are unenrolled students and auto-add is selected
        if request.form.get('auto_enroll') == '1' and not_enrolled_students:
            # Check course capacity
            current_enrolled = CourseEnrollment.query.filter_by(course_code=course_code).count()
            if current_enrolled + len(not_enrolled_students) > course.capacity:
                flash('The number of students to add exceeds the course capacity limit, not automatically added.')
            else:
                # Auto add students
                for student in not_enrolled_students:
                    enrollment = CourseEnrollment(
                        course_code=course_code,
                        student_id=student.id
                    )
                    db.session.add(enrollment)
                db.session.commit()
                flash(f'Successfully added {len(not_enrolled_students)} students to the course automatically.')
                enrolled_students.extend(not_enrolled_students)
                not_enrolled_students = []
        
        # Prepare import result data structure
        imported_result = {
            'total_students': len(csv_data),
            'existing_students': len(enrolled_students) + len(not_enrolled_students),
            'missing_students': len(errors),
            'already_enrolled': len(enrolled_students),
            'newly_enrolled': len(not_enrolled_students),
            'enrolled_students': enrolled_students,
            'not_enrolled_students': not_enrolled_students,
            'missing_students_list': []
        }
        
        # Convert error messages to student list format
        if errors:
            for error in errors:
                # Try to parse student information
                try:
                    # Simple parsing of student data from error messages
                    # Format: "Student not found: {'student_id': '123', 'username': 'John Doe', 'email': 'xxx@polyu.edu.hk}"
                    student_data = eval(error[15:])  # Remove "Student not found: " prefix
                    imported_result['missing_students_list'].append({
                        'id': student_data.get('student_id', ''),
                        'username': student_data.get('username', ''),
                        'email': student_data.get('email', '')
                    })
                except:
                    # If parsing fails, add a basic entry
                    imported_result['missing_students_list'].append({
                        'id': '',
                        'username': '',
                        'email': error
                    })
        
        # Display import results
        return render_template('import_students.html', 
                              course=course, 
                              imported_result=imported_result)
    
    return render_template('import_students.html', course=course)