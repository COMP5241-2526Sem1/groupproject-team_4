from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# 为 Flask 应用设置 secret_key，解决 session 报错
app.secret_key = 'your_secret_key_123456789'

# 初始化数据库对象
from models import User, Course, CourseEnrollment, Activity, Submission, Grade, Notification, SystemLog
from models import db
db.init_app(app)

# 注册auth蓝图
from routes.auth import auth_bp
app.register_blueprint(auth_bp)
from routes.course import course_bp
app.register_blueprint(course_bp)

# 路由：登录和注册页面
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

# 跳转后的角色首页（占位页面）
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
