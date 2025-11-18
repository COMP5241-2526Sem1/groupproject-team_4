from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, db
import re

# 创建蓝图
auth_bp = Blueprint('auth', __name__)

# 邮箱格式校验（支持所有标准邮箱格式）
def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)

# 密码强度校验（必须包含字母和数字，可有特殊符号，不能全数字）
def is_valid_password(password):
    if password.isdigit():
        return False
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+=-]{6,}$'
    return re.match(pattern, password)

# 注册接口
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    email = data.get('email')

    if not username or not password or not role or not email:
        return jsonify({'msg': '用户名、密码、角色和邮箱不能为空'}), 400

    if not is_valid_email(email):
        return jsonify({'msg': '邮箱格式不正确'}), 400

    if not is_valid_password(password):
        return jsonify({'msg': '密码必须包含字母和数字，且不能全为数字'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': '用户名已存在'}), 400

    password_hash = generate_password_hash(password)
    user = User(username=username, password_hash=password_hash, role=role, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': '注册成功'}), 201

# 登录接口
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    user = User.query.filter_by(username=username, role=role).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'msg': '用户名、密码或角色错误'}), 401
    session['user_id'] = user.id
    session['role'] = user.role
    session['username'] = user.username
    return jsonify({'msg': '登录成功', 'role': user.role}), 200

# 登出接口
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# 获取当前用户信息
@auth_bp.route('/user/profile', methods=['GET'])
def get_user_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'msg': '未登录'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': '用户不存在'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'role': user.role,
        'email': user.email,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None
    }), 200
