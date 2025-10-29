from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Set secret_key for Flask app to avoid session errors
app.secret_key = 'your_secret_key_123456789'

# Initialize database object
from models import User, Course, CourseEnrollment, Activity, Submission, Grade, Notification, SystemLog
from models import db
db.init_app(app)

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

@app.route('/')
def index():
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
