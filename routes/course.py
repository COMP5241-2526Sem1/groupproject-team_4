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
from models.word_cloud import WordCloud
from models.minigame import Minigame
from models.attempt import Attempt
from database import db

course_bp = Blueprint('course', __name__)
# THIS IS RESTFUL API, NOT A VISABLE WEB PAGE!!!

# Get all available course (not enrolled)
@course_bp.route('/course/available', methods=['GET'])
def get_available_course():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': 'Not logged in'}), 401
    # Enrolled course codes
    enrolled_codes = [e.course_code for e in CourseEnrollment.query.filter_by(student_id=student_id).all()]
    # Available course (not enrolled and not full)
    # Weekday sorting helper dictionary
    weekday_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    course = Course.query.filter(~Course.code.in_(enrolled_codes)).all()
    course = sorted(course, key=lambda c: (weekday_order.get(c.day_of_week, 99), c.start_time))
    result = []
    for c in course:
        enrolled_count = CourseEnrollment.query.filter_by(course_code=c.code).count()
        result.append({
            'code': c.code,
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
    course = [Course.query.get(e.course_code) for e in enrollments]
    weekday_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    course_sorted = sorted(course, key=lambda c: (weekday_order.get(c.day_of_week, 99), c.start_time))
    result = []
    for c in course_sorted:
        result.append({
            'code': c.code,
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
    course_code = request.json.get('course_code')
    course = Course.query.get(course_code)
    if not course:
        return jsonify({'msg': 'Course does not exist'}), 404
    # Check if already selected
    if CourseEnrollment.query.filter_by(student_id=student_id, course_code=course_code).first():
        return jsonify({'msg': 'Already enrolled in this course'}), 400
    # Check capacity
    enrolled_count = CourseEnrollment.query.filter_by(course_code=course_code).count()
    if enrolled_count >= course.capacity:
        return jsonify({'msg': 'Course is full'}), 400
    # Check credits and course count
    enrollments = CourseEnrollment.query.filter_by(student_id=student_id).all()
    total_credits = sum(Course.query.get(e.course_code).credit for e in enrollments)
    if total_credits + course.credit > 18:
        return jsonify({'msg': 'Credit limit exceeded, maximum 18 credits'}), 400
    if len(enrollments) >= 6:
        return jsonify({'msg': 'Maximum 6 courses allowed'}), 400
    # Check time conflict
    for e in enrollments:
        c2 = Course.query.get(e.course_code)
        if c2.day_of_week == course.day_of_week:
            # Conflict if time overlaps
            if not (course.end_time <= c2.start_time or course.start_time >= c2.end_time):
                return jsonify({'msg': 'Course time conflict, please select another course'}), 400
    # Add course enrollment
    new_enroll = CourseEnrollment(course_code=course_code, student_id=student_id)
    db.session.add(new_enroll)
    db.session.commit()
    return jsonify({'msg': 'Course selection successful'})

# drop
@course_bp.route('/course/drop', methods=['POST'])
def drop_course():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': 'Not logged in'}), 401
    course_code = request.json.get('course_code')
    enroll = CourseEnrollment.query.filter_by(student_id=student_id, course_code=course_code).first()
    if not enroll:
        return jsonify({'msg': 'not enrolled in this course'}), 400
    db.session.delete(enroll)
    db.session.commit()
    return jsonify({'msg': 'course dropped successfully!'})

# Dashboard route for student course dashboard
@course_bp.route('/course/<course_code>/dashboard', methods=['GET'])
def course_dashboard(course_code):
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': 'Not logged in'}), 401
    
    # Check if student is enrolled in this course
    enrollment = CourseEnrollment.query.filter_by(student_id=student_id, course_code=course_code).first()
    if not enrollment:
        return jsonify({'msg': 'Not enrolled in this course'}), 403
    
    # Get course info
    course = Course.query.get(course_code)
    if not course:
        return jsonify({'msg': 'Course not found'}), 404
    
    # Get student attempts for activities (quiz, word cloud, poll, mini games)
    quiz_attempts = Attempt.query.join(Quiz).filter(
        Attempt.user_id == student_id,
        Quiz.course_code == course_code
    ).count()
    
    word_cloud_attempts = Submission.query.join(WordCloud).filter(
        Submission.user_id == student_id,
        WordCloud.course_code == course_code
    ).count()
    
    poll_attempts = Submission.query.join(Poll).filter(
        Submission.user_id == student_id,
        Poll.course_code == course_code
    ).count()
    
    mini_game_attempts = Submission.query.join(Minigame).filter(
        Submission.user_id == student_id,
        Minigame.course_code == course_code
    ).count()
    
    total_completed = quiz_attempts + word_cloud_attempts + poll_attempts + mini_game_attempts
    total_available = 5  # Total available activities
    
    # Get leaderboard data - class participation by total attempts
    leaderboard_data = []
    enrollments = CourseEnrollment.query.filter_by(course_code=course_code).all()
    
    for enrollment in enrollments:
        student = User.query.get(enrollment.student_id)
        if student:
            # Count total attempts for this student
            student_quiz_attempts = Attempt.query.join(Quiz).filter(
                Attempt.user_id == student.id,
                Quiz.course_code == course_code
            ).count()
            
            student_word_cloud_attempts = Submission.query.join(WordCloud).filter(
                Submission.user_id == student.id,
                WordCloud.course_code == course_code
            ).count()
            
            student_poll_attempts = Submission.query.join(Poll).filter(
                Submission.user_id == student.id,
                Poll.course_code == course_code
            ).count()
            
            student_mini_game_attempts = Submission.query.join(Minigame).filter(
                Submission.user_id == student.id,
                Minigame.course_code == course_code
            ).count()
            
            total_attempts = (student_quiz_attempts + student_word_cloud_attempts + 
                            student_poll_attempts + student_mini_game_attempts)
            
            leaderboard_data.append({
                'name': student.username,
                'attempts': total_attempts
            })
    
    # Sort by attempts (descending)
    leaderboard_data.sort(key=lambda x: x['attempts'], reverse=True)
    
    return render_template('dashboard.html', 
                         course=course,
                         completed_activities=total_completed,
                         total_activities=total_available,
                         leaderboard_data=leaderboard_data)