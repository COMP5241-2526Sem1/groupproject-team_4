from flask import Flask, render_template, redirect, url_for
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

from models import User, Course, CourseEnrollment, Activity, Submission, Grade, Notification, SystemLog
try:
    with app.app_context():
        print(app.app_context)
        res = db.create_all()
        print(res)
        # Enable Row Level Security for all tables
        tables = db.session.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")).fetchall()
        for table in tables:
            db.session.execute(text(f'ALTER TABLE {table[0]} ENABLE ROW LEVEL SECURITY;'))
        from database import create_sample
        create_sample()
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
    return render_template('role_home.html', role='Teacher')

@app.route('/admin_home')
def admin_home():
    return render_template('role_home.html', role='Admin')

@app.route('/course/<int:course_id>')
def course_by_id(course_id):
    course = Course.query.get_or_404(course_id)
    return render_template('course_home.html', course=course)


@app.route('/course/<string:course_code>')
def course_by_code(course_code):
    course = Course.query.filter_by(code=course_code).first_or_404()
    return render_template('course_home.html', course=course)

@app.route('/')
def index():
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)