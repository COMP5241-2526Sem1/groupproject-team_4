from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from functools import wraps
from database import db
from models.user import User
from models.course import Course
from models.course_enrollment import CourseEnrollment
import csv
import io
import random
import string

# 创建教师课程管理蓝图
teacher_course_bp = Blueprint('teacher_course', __name__)

# 认证装饰器：检查用户是否已登录
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('您需要先登录才能访问此页面。')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# 认证装饰器：检查用户是否是教师
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 首先检查是否已登录
        if 'user_id' not in session:
            flash('您需要先登录才能访问此页面。')
            return redirect(url_for('auth.login'))
        
        # 获取用户角色
        user = User.query.get(session['user_id'])
        if not user or user.role != 'teacher':
            flash('您需要是教师才能访问此页面。')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

# 生成随机课程代码
def generate_course_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# 教师课程主页 - 显示所有课程
@teacher_course_bp.route('/teacher_course')
@login_required
@teacher_required
def teacher_course_home():
    # 获取当前教师ID
    teacher_id = session['user_id']
    
    # 获取教师自己创建的课程
    my_courses = Course.query.filter_by(teacher_id=teacher_id).all()
    
    # 获取其他教师创建的课程
    other_courses = Course.query.filter(Course.teacher_id != teacher_id).all()
    
    return render_template('teacher_course_home.html', my_courses=my_courses, other_courses=other_courses)

# 获取教师课程列表的API端点（用于下拉菜单）
@teacher_course_bp.route('/teacher_course/list')
@login_required
@teacher_required
def get_teacher_courses():
    # 获取当前教师ID
    teacher_id = session['user_id']
    
    # 获取教师自己创建的课程
    courses = Course.query.filter_by(teacher_id=teacher_id).all()
    
    # 返回JSON格式的课程列表
    course_list = [{
        'id': course.id,
        'name': course.name,
        'code': course.code
    } for course in courses]
    
    return jsonify(course_list)

# 教师课程详细页面
@teacher_course_bp.route('/teacher_course/<int:course_id>')
@login_required
@teacher_required
def teacher_course_detail(course_id):
    # 获取课程信息
    course = Course.query.get_or_404(course_id)
    
    # 检查是否是该课程的教师
    if course.teacher_id != session['user_id']:
        flash('您不是此课程的教师，无法访问此页面。')
        return redirect(url_for('teacher_course.teacher_course_home'))
    
    # 获取课程的学生数量
    enrolled_count = CourseEnrollment.query.filter_by(course_id=course_id).count()
    
    return render_template('teacher_course_detail.html', course=course, enrolled_count=enrolled_count)

# 创建新课程页面
@teacher_course_bp.route('/teacher_course/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_course():
    if request.method == 'POST':
        # 获取表单数据
        name = request.form['name']
        description = request.form['description']
        credit = int(request.form['credit'])
        capacity = int(request.form['capacity'])
        day_of_week = request.form['day_of_week']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        department_id = request.form.get('department_id')  # 可选字段
        
        # 生成唯一的课程代码
        code = generate_course_code()
        while Course.query.filter_by(code=code).first():
            code = generate_course_code()
        
        # 创建新课程
        new_course = Course(
            code=code,
            name=name,
            description=description,
            teacher_id=session['user_id'],
            credit=credit,
            capacity=capacity,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            department_id=department_id if department_id else None
        )
        
        # 保存到数据库
        db.session.add(new_course)
        db.session.commit()
        
        flash('课程创建成功！')
        return redirect(url_for('teacher_course.teacher_course_detail', course_id=new_course.id))
    
    return render_template('create_course.html')

# 已注册学生列表页面
@teacher_course_bp.route('/teacher_course/<int:course_id>/enrolled_list', methods=['GET', 'POST'])
@login_required
@teacher_required
def enrolled_list(course_id):
    # 获取课程信息
    course = Course.query.get_or_404(course_id)
    
    # 检查是否是该课程的教师
    if course.teacher_id != session['user_id']:
        flash('您不是此课程的教师，无法访问此页面。')
        return redirect(url_for('teacher_course.teacher_course_home'))
    
    # 获取搜索条件
    department_filter = request.args.get('department')
    
    # 获取已注册的学生
    enrolled_students = db.session.query(User).join(
        CourseEnrollment, User.id == CourseEnrollment.student_id
    ).filter(
        CourseEnrollment.course_id == course_id
    )
    
    # 应用部门过滤
    if department_filter:
        enrolled_students = enrolled_students.filter(User.department == department_filter)
    
    enrolled_students = enrolled_students.all()
    
    # 处理删除学生操作
    if request.method == 'POST':
        student_ids = request.form.getlist('students[]')
        if student_ids:
            # 删除选中的学生注册记录
            CourseEnrollment.query.filter(
                CourseEnrollment.course_id == course_id,
                CourseEnrollment.student_id.in_(student_ids)
            ).delete(synchronize_session=False)
            db.session.commit()
            flash(f'已从课程中移除 {len(student_ids)} 名学生。')
        return redirect(url_for('teacher_course.enrolled_list', course_id=course_id))
    
    return render_template('enrolled_list.html', course=course, students=enrolled_students)

# 未注册学生列表页面
@teacher_course_bp.route('/teacher_course/<int:course_id>/not_enrolled_list', methods=['GET', 'POST'])
@login_required
@teacher_required
def not_enrolled_list(course_id):
    # 获取课程信息
    course = Course.query.get_or_404(course_id)
    
    # 检查是否是该课程的教师
    if course.teacher_id != session['user_id']:
        flash('您不是此课程的教师，无法访问此页面。')
        return redirect(url_for('teacher_course.teacher_course_home'))
    
    # 获取搜索条件
    department_filter = request.args.get('department')
    
    # 获取未注册的学生
    not_enrolled_students = User.query.filter(
        User.role == 'student',
        User.id.notin_(
            db.session.query(CourseEnrollment.student_id)
            .filter(CourseEnrollment.course_id == course_id)
        )
    )
    
    # 应用部门过滤
    if department_filter:
        not_enrolled_students = not_enrolled_students.filter(User.department == department_filter)
    
    not_enrolled_students = not_enrolled_students.all()
    
    # 处理添加学生操作
    if request.method == 'POST':
        student_ids = request.form.getlist('students[]')
        if student_ids:
            # 检查课程容量
            current_enrolled = CourseEnrollment.query.filter_by(course_id=course_id).count()
            if current_enrolled + len(student_ids) > course.capacity:
                flash('添加的学生数量超过了课程容量限制。')
                return redirect(url_for('teacher_course.not_enrolled_list', course_id=course_id))
            
            # 添加选中的学生
            for student_id in student_ids:
                enrollment = CourseEnrollment(
                    course_id=course_id,
                    student_id=student_id
                )
                db.session.add(enrollment)
            db.session.commit()
            flash(f'已成功添加 {len(student_ids)} 名学生到课程中。')
        return redirect(url_for('teacher_course.not_enrolled_list', course_id=course_id))
    
    return render_template('not_enrolled_list.html', course=course, students=not_enrolled_students)

# CSV导入学生页面
@teacher_course_bp.route('/teacher_course/<int:course_id>/import_students', methods=['GET', 'POST'])
@login_required
@teacher_required
def import_students(course_id):
    # 获取课程信息
    course = Course.query.get_or_404(course_id)
    
    # 检查是否是该课程的教师
    if course.teacher_id != session['user_id']:
        flash('您不是此课程的教师，无法访问此页面。')
        return redirect(url_for('teacher_course.teacher_course_home'))
    
    # 处理CSV文件上传
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'csv_file' not in request.files or request.files['csv_file'].filename == '':
            flash('请选择一个CSV文件上传。')
            return redirect(request.url)
        
        csv_file = request.files['csv_file']
        
        # 检查文件类型
        if not csv_file.filename.endswith('.csv'):
            flash('请上传CSV格式的文件。')
            return redirect(request.url)
        
        # 解析CSV文件
        csv_data = []
        try:
            # 读取CSV文件内容
            stream = io.StringIO(csv_file.stream.read().decode('utf-8'))
            reader = csv.DictReader(stream)
            
            # 检查CSV格式是否正确
            required_columns = ['student_id', 'email']  # 至少需要学生ID或邮箱
            if not any(col in reader.fieldnames for col in required_columns):
                flash('CSV文件格式不正确，至少需要包含student_id或email列。')
                return redirect(request.url)
            
            csv_data = list(reader)
        except Exception as e:
            flash(f'解析CSV文件时出错: {str(e)}')
            return redirect(request.url)
        
        # 处理学生数据
        enrolled_students = []
        not_enrolled_students = []
        errors = []
        
        for row in csv_data:
            student = None
            
            # 尝试通过学生ID查找
            if 'student_id' in row and row['student_id']:
                # 将student_id转换为整数类型
                try:
                    student_id = int(row['student_id'])
                    student = User.query.filter_by(id=student_id, role='student').first()
                except ValueError:
                    # 如果转换失败，继续尝试通过邮箱查找
                    student = None
            
            # 如果没有找到，尝试通过邮箱查找
            if not student and 'email' in row and row['email']:
                student = User.query.filter_by(email=row['email'], role='student').first()
            
            if not student:
                errors.append(f"找不到学生: {row}")
                continue
            
            # 检查学生是否已注册该课程
            enrollment = CourseEnrollment.query.filter_by(
                course_id=course_id,
                student_id=student.id
            ).first()
            
            if enrollment:
                enrolled_students.append(student)
            else:
                not_enrolled_students.append(student)
        
        # 如果有未注册的学生且选择了自动添加
        if request.form.get('auto_enroll') == '1' and not_enrolled_students:
            # 检查课程容量
            current_enrolled = CourseEnrollment.query.filter_by(course_id=course_id).count()
            if current_enrolled + len(not_enrolled_students) > course.capacity:
                flash('添加的学生数量超过了课程容量限制，未自动添加。')
            else:
                # 自动添加学生
                for student in not_enrolled_students:
                    enrollment = CourseEnrollment(
                        course_id=course_id,
                        student_id=student.id
                    )
                    db.session.add(enrollment)
                db.session.commit()
                flash(f'已自动添加 {len(not_enrolled_students)} 名学生到课程中。')
                enrolled_students.extend(not_enrolled_students)
                not_enrolled_students = []
        
        # 准备导入结果数据结构
        imported_result = {
            'total_students': len(csv_data),
            'existing_students': len(enrolled_students) + len(not_enrolled_students),
            'missing_students': len(errors),
            'already_enrolled': len(enrolled_students),
            'newly_enrolled': len(not_enrolled_students),
            'enrolled_students': enrolled_students,
            'not_enrolled_students': not_enrolled_students,
            'missing_students_list': []
        }
        
        # 转换错误信息为学生列表格式
        if errors:
            for error in errors:
                # 尝试解析出学生信息
                try:
                    # 简单解析错误信息中的学生数据
                    # 格式: "找不到学生: {'student_id': '123', 'username': '张三', 'email': 'xxx@polyu.edu.hk}"
                    student_data = eval(error[5:])  # 去掉"找不到学生: "前缀
                    imported_result['missing_students_list'].append({
                        'id': student_data.get('student_id', ''),
                        'username': student_data.get('username', ''),
                        'email': student_data.get('email', '')
                    })
                except:
                    # 如果解析失败，添加一个基本条目
                    imported_result['missing_students_list'].append({
                        'id': '',
                        'username': '',
                        'email': error
                    })
        
        # 显示导入结果
        return render_template('import_students.html', 
                              course=course, 
                              imported_result=imported_result)
    
    return render_template('import_students.html', course=course)