from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User, db
import re

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Email format validation (supports all standard email formats)
def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)

# Password strength validation (must contain letters and numbers, can include special characters, cannot be all digits)
def is_valid_password(password):
    if password.isdigit():
        return False
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+=-]{6,}$'
    return re.match(pattern, password)

# Registration endpoint
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    email = data.get('email')

    if not username or not password or not role or not email:
        return jsonify({'msg': 'Username, password, role, and email cannot be empty'}), 400

    if not is_valid_email(email):
        return jsonify({'msg': 'Invalid email format'}), 400

    if not is_valid_password(password):
        return jsonify({'msg': 'Password must contain letters and numbers, and cannot be all digits'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Username already exists'}), 400

    password_hash = generate_password_hash(password)
    user = User(username=username, password_hash=password_hash, role=role, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'msg': 'Registration successful'}), 201

# Login endpoint
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
    return jsonify({'msg': '登录成功', 'role': user.role}), 200

# logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))
