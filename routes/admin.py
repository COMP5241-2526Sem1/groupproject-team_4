from flask import Blueprint, request, jsonify, session
from models.user import User, db
from werkzeug.security import generate_password_hash
import re

admin_bp = Blueprint('admin', __name__)

# 邮箱格式校验
def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email)

# 密码强度校验
def is_valid_password(password):
    if password.isdigit():
        return False
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+=-]{6,}$'
    return re.match(pattern, password)

# 获取指定角色的所有用户
@admin_bp.route('/admin/users/<role>', methods=['GET'])
def get_users_by_role(role):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'msg': 'Not logged in'}), 401
    
    # Verify admin role
    admin = User.query.get(user_id)
    if not admin or admin.role != 'admin':
        return jsonify({'msg': 'Insufficient permissions'}), 403
    
    if role not in ['teacher', 'student']:
        return jsonify({'msg': 'Invalid role type'}), 400
    
    users = User.query.filter_by(role=role).all()
    
    users_list = [{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None
    } for user in users]
    
    return jsonify({'users': users_list}), 200

# 添加新用户
@admin_bp.route('/admin/users', methods=['POST'])
def add_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'msg': 'Not logged in'}), 401
    
    # Verify admin role
    admin = User.query.get(user_id)
    if not admin or admin.role != 'admin':
        return jsonify({'msg': 'Insufficient permissions'}), 403
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')
    
    if not username or not password or not email or not role:
        return jsonify({'msg': 'All fields are required'}), 400
    
    if role not in ['teacher', 'student']:
        return jsonify({'msg': 'Invalid role type'}), 400
    
    if not is_valid_email(email):
        return jsonify({'msg': 'Invalid email format'}), 400
    
    if not is_valid_password(password):
        return jsonify({'msg': 'Password must contain letters and numbers'}), 400
    
    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'msg': 'Username already exists'}), 400
    
    # 创建新用户
    password_hash = generate_password_hash(password)
    new_user = User(
        username=username,
        password_hash=password_hash,
        email=email,
        role=role
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'msg': 'User added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Add failed: {str(e)}'}), 500

# 删除用户
@admin_bp.route('/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    admin_id = session.get('user_id')
    if not admin_id:
        return jsonify({'msg': 'Not logged in'}), 401
    
    # Verify admin role
    admin = User.query.get(admin_id)
    if not admin or admin.role != 'admin':
        return jsonify({'msg': 'Insufficient permissions'}), 403
    
    # Cannot delete yourself
    if admin_id == user_id:
        return jsonify({'msg': 'Cannot delete your own account'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    # Cannot delete other admins
    if user.role == 'admin':
        return jsonify({'msg': 'Cannot delete admin accounts'}), 400
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'msg': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'Delete failed: {str(e)}'}), 500
