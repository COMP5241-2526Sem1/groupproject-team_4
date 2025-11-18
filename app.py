from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# 为 Flask 应用设置 secret_key，解决 session 报错
app.secret_key = 'your_secret_key_123456789'

# 添加全局请求日志
@app.before_request
def log_request():
    print(f"\n{'='*80}")
    print(f"REQUEST: {request.method} {request.path}")
    print(f"From: {request.remote_addr}")
    if request.is_json:
        print(f"JSON Data: {request.get_json()}")
    print(f"{'='*80}\n")

# 初始化数据库对象
from models import User, Course, CourseEnrollment, Activity, Submission, Grade, Notification, SystemLog
from models.user import db
db.init_app(app)

# 注册auth蓝图
from routes.auth import auth_bp
app.register_blueprint(auth_bp)
from routes.course import course_bp
app.register_blueprint(course_bp)
from routes.activity import activity_bp
app.register_blueprint(activity_bp)
from routes.admin import admin_bp
app.register_blueprint(admin_bp)

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
    from flask import session
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login_page'))
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('login_page'))
    
    return render_template('student_home.html', 
                         username=user.username,
                         user_id=user.id,
                         email=user.email or '未设置',
                         role=user.role)

@app.route('/teacher_home')
def teacher_home():
    user_id = session.get('user_id')
    username = session.get('username', 'Teacher')
    
    user = User.query.get(user_id) if user_id else None
    email = user.email if user else 'N/A'
    
    return render_template('teacher_home.html', 
                         username=username, 
                         user_id=user_id, 
                         email=email)

@app.route('/admin_home')
def admin_home():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return redirect('/login')
    
    return render_template('admin_home.html')

@app.route('/')
def index():
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
