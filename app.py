from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import text
from database import db


app = Flask(__name__)

# Set secret_key for Flask app to avoid session errors
app.secret_key = 'your_secret_key_123456789'

# Initialize database object
app.config.from_object(Config)
db.init_app(app)

try:
    with app.app_context():
        db.session.execute(text('SELECT version();'))
        print("PostgreSQL Database Connected Successfully!!!")
except Exception as e:
    print(f"PostgreSQL Database Connection Failed!: {e}")

from models import *
try:
    with app.app_context():
        print(app.app_context)
        res = db.create_all()
        print("create_all tables---")
        print(res)
        print("create_all tables---")
        # Enable Row Level Security for all tables

        #create_sample()
except Exception as e:
    print(f"not create!: {e}")

def create_sample():
    # Insert sample users
    sample_users = [
        {'username': 'student1', 'password_hash': 'hashed_password_1', 'role': 'student', 'email': 'student1@example.com'},
        {'username': 'teacher1', 'password_hash': 'hashed_password_2', 'role': 'teacher', 'email': 'teacher1@example.com'},
        {'username': 'admin1', 'password_hash': 'hashed_password_3', 'role': 'admin', 'email': 'admin1@example.com'}
    ]
    for user_data in sample_users:
        user = User(
            username=user_data['username'],
            password_hash=user_data['password_hash'],
            role=user_data['role'],
            email=user_data['email']
        )
        with app.app_context():
            db.session.add(user)
            db.session.commit()

    # Insert sample courses
    sample_courses = [
        {'name': 'Introduction to Programming', 'description': 'Basic programming concepts', 'teacher_id': 1, 'credit': 3, 'capacity': 30, 'day_of_week': 'Mon', 'start_time': '09:00:00', 'end_time': '11:00:00'},
        {'name': 'Data Structures', 'description': 'Fundamental data structures', 'teacher_id': 1, 'credit': 4, 'capacity': 25, 'day_of_week': 'Tue', 'start_time': '13:00:00', 'end_time': '15:00:00'},
        {'name': 'Algorithms', 'description': 'Algorithm design and analysis', 'teacher_id': 2, 'credit': 4, 'capacity': 20, 'day_of_week': 'Wed', 'start_time': '10:00:00', 'end_time': '12:00:00'}
    ]
    for course_data in sample_courses:
        course = Course(
            name=course_data['name'],
            description=course_data['description'],
            teacher_id=course_data['teacher_id'],
            credit=course_data['credit'],
            capacity=course_data['capacity'],
            day_of_week=course_data['day_of_week'],
            start_time=course_data['start_time'],
            end_time=course_data['end_time']
        )
        with app.app_context():
            db.session.add(course)
            db.session.commit()

#create_sample()

# Register auth blueprint
from routes.auth import auth_bp
app.register_blueprint(auth_bp)
from routes.course import course_bp
app.register_blueprint(course_bp)
# Register quiz and poll blueprints
from routes.quiz_routes import quiz_bp
app.register_blueprint(quiz_bp)
from routes.poll_routes import poll_bp
app.register_blueprint(poll_bp)
# Register course registration blueprint
from routes.course_registration import course_registration_bp
app.register_blueprint(course_registration_bp)
# Register teacher course blueprint
from routes.teacher_course import teacher_course_bp
app.register_blueprint(teacher_course_bp)
# Register teacher quiz blueprint
from routes.teacher_quiz_routes import teacher_quiz_bp
app.register_blueprint(teacher_quiz_bp)
# Register word cloud blueprint
from routes.word_cloud_routes import word_cloud_bp
app.register_blueprint(word_cloud_bp)
# Register AI routes blueprint
from routes.ai_routes import ai_bp
app.register_blueprint(ai_bp)
# Register short answer routes blueprint
from routes.short_answer_routes import short_answer_bp
app.register_blueprint(short_answer_bp)

# Routes: Login and registration pages
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

# Role-specific home pages (placeholder)
@app.route('/student_home')
def student_home():
    return render_template('student_home.html')

@app.route('/teacher_home')
def teacher_home():
    from models.course import Course
    from flask import session
    # Get current teacher ID from session
    if 'user_id' in session:
        teacher_id = session['user_id']
        # Get courses created by the teacher
        my_courses = Course.query.filter_by(teacher_id=teacher_id).all()
        # Get courses created by other teachers
        other_courses = Course.query.filter(Course.teacher_id != teacher_id).all()
        return render_template('teacher_home.html', my_courses=my_courses, other_courses=other_courses)
    return render_template('teacher_home.html', my_courses=[], other_courses=[])

@app.route('/admin_home')
def admin_home():
    return render_template('role_home.html', role='Admin')




@app.route('/course/<string:course_code>')
def course_by_code(course_code):
    course = Course.query.filter_by(code=course_code).first_or_404()
    return render_template('course_home.html', course=course)

@app.route('/')
def index():
    return redirect('/login')

# Route for serving favicon.ico
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Route for testing Add Question functionality
@app.route('/test_add_question')
def test_add_question():
    return send_from_directory('.', 'test_add_question_js.html')

@app.route('/test_add_question_function')
def test_add_question_function():
    return send_from_directory('.', 'test_add_question_function.html')

@app.route('/test_function_exists')
def test_function_exists():
    return send_from_directory('.', 'test_function_exists.html')

@app.route('/test_quiz_functions')
def test_quiz_functions():
    return send_from_directory('.', 'test_quiz_functions.html')

if __name__ == '__main__':
    app.run(debug=True)