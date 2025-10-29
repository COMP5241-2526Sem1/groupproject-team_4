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

except Exception as e:
    print(f"not create!: {e}")



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