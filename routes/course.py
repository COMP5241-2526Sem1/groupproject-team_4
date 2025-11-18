from flask import Blueprint, request, jsonify, session
from models.course import Course
from models.course_enrollment import CourseEnrollment
from models.user import User, db
import csv
import io
from datetime import datetime, time

course_bp = Blueprint('course', __name__)

# 获取所有可选课程（未选的课程）
@course_bp.route('/courses/available', methods=['GET'])
def get_available_courses():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': '未登录'}), 401
    # 已选课程id
    enrolled_ids = [e.course_id for e in CourseEnrollment.query.filter_by(student_id=student_id).all()]
    # 可选课程（未选且未满员）
    # 星期排序辅助字典
    weekday_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    courses = Course.query.filter(~Course.id.in_(enrolled_ids)).all()
    courses = sorted(courses, key=lambda c: (weekday_order.get(c.day_of_week, 99), c.start_time))
    result = []
    for c in courses:
        enrolled_count = CourseEnrollment.query.filter_by(course_id=c.id).count()
        result.append({
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'credit': c.credit,
            'capacity': c.capacity,
            'enrolled': enrolled_count,
            'teacher_id': c.teacher_id,
            'day_of_week': c.day_of_week,
            'start_time': str(c.start_time) if c.start_time else '',
            'end_time': str(c.end_time) if c.end_time else ''
        })
    return jsonify(result)

# 获取学生已选课程列表
@course_bp.route('/courses/my', methods=['GET'])
def get_my_courses():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': '未登录'}), 401
    enrollments = CourseEnrollment.query.filter_by(student_id=student_id).all()
    # 取出所有已选课程对象
    courses = [Course.query.get(e.course_id) for e in enrollments]
    weekday_order = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    courses_sorted = sorted(courses, key=lambda c: (weekday_order.get(c.day_of_week, 99), c.start_time))
    result = []
    for c in courses_sorted:
        result.append({
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'credit': c.credit,
            'capacity': c.capacity,
            'teacher_id': c.teacher_id,
            'day_of_week': c.day_of_week,
            'start_time': str(c.start_time) if c.start_time else '',
            'end_time': str(c.end_time) if c.end_time else ''
        })
    return jsonify(result)

# 选课接口
@course_bp.route('/courses/add', methods=['POST'])
def add_course():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': '未登录'}), 401
    course_id = request.json.get('course_id')
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'msg': '课程不存在'}), 404
    # 校验是否已选
    if CourseEnrollment.query.filter_by(student_id=student_id, course_id=course_id).first():
        return jsonify({'msg': '已选该课程'}), 400
    # 校验人数
    enrolled_count = CourseEnrollment.query.filter_by(course_id=course_id).count()
    if enrolled_count >= course.capacity:
        return jsonify({'msg': '课程人数已满'}), 400
    # 校验学分和课程数
    enrollments = CourseEnrollment.query.filter_by(student_id=student_id).all()
    total_credits = sum(Course.query.get(e.course_id).credit for e in enrollments)
    if total_credits + course.credit > 18:
        return jsonify({'msg': '学分超限，最多18学分'}), 400
    if len(enrollments) >= 6:
        return jsonify({'msg': '最多只能选6门课程'}), 400
    # 校验时间冲突
    for e in enrollments:
        c2 = Course.query.get(e.course_id)
        if c2.day_of_week == course.day_of_week:
            # 时间有重叠则冲突
            if not (course.end_time <= c2.start_time or course.start_time >= c2.end_time):
                return jsonify({'msg': '课程时间冲突，请选择其他课程'}), 400
    # 添加选课
    new_enroll = CourseEnrollment(course_id=course_id, student_id=student_id)
    db.session.add(new_enroll)
    db.session.commit()
    return jsonify({'msg': '选课成功'})

# 退课接口
@course_bp.route('/courses/drop', methods=['POST'])
def drop_course():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': '未登录'}), 401
    course_id = request.json.get('course_id')
    enroll = CourseEnrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if not enroll:
        return jsonify({'msg': '未选该课程'}), 400
    db.session.delete(enroll)
    db.session.commit()
    return jsonify({'msg': '退课成功'})

# 获取教师所教授的所有课程
@course_bp.route('/courses/teacher/my', methods=['GET'])
def get_teacher_courses():
    teacher_id = session.get('user_id')
    if not teacher_id:
        return jsonify({'msg': '未登录'}), 401
    # 查询该教师的所有课程
    courses = Course.query.filter_by(teacher_id=teacher_id).all()
    # 按星期和时间排序
    weekday_order = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7,
                     'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
    courses_sorted = sorted(courses, key=lambda c: (weekday_order.get(c.day_of_week, 99), c.start_time))
    
    result = []
    for c in courses_sorted:
        # 统计该课程的选课人数
        enrolled_count = CourseEnrollment.query.filter_by(course_id=c.id).count()
        result.append({
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'credit': c.credit,
            'capacity': c.capacity,
            'enrolled': enrolled_count,
            'day_of_week': c.day_of_week,
            'start_time': str(c.start_time) if c.start_time else '',
            'end_time': str(c.end_time) if c.end_time else ''
        })
    return jsonify(result)

# 教师创建新课程
@course_bp.route('/courses/teacher/create', methods=['POST'])
def create_course():
    teacher_id = session.get('user_id')
    if not teacher_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    try:
        data = request.json
        name = data.get('name')
        description = data.get('description', '')
        credit = data.get('credit')
        capacity = data.get('capacity')
        day_of_week = data.get('day_of_week')
        start_time_str = data.get('start_time')
        end_time_str = data.get('end_time')
        
        # 验证必填字段
        if not all([name, credit, capacity, day_of_week, start_time_str, end_time_str]):
            return jsonify({'msg': '请填写所有必填字段', 'success': False}), 400
        
        # 转换数字类型
        try:
            credit = int(credit)
            capacity = int(capacity)
        except (ValueError, TypeError):
            return jsonify({'msg': '学分和容量必须是数字', 'success': False}), 400
        
        # 验证学分范围
        if credit < 1 or credit > 6:
            return jsonify({'msg': '学分必须在1-6之间', 'success': False}), 400
        
        # 验证容量
        if capacity < 1 or capacity > 200:
            return jsonify({'msg': '课程容量必须在1-200之间', 'success': False}), 400
        
        # 转换时间格式
        try:
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
        except ValueError as e:
            return jsonify({'msg': f'时间格式不正确: {str(e)}', 'success': False}), 400
        
        # 验证时间逻辑
        if start_time >= end_time:
            return jsonify({'msg': '结束时间必须晚于开始时间', 'success': False}), 400
        
        # 创建课程
        new_course = Course(
            name=name,
            description=description,
            teacher_id=teacher_id,
            credit=credit,
            capacity=capacity,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time
        )
        
        db.session.add(new_course)
        db.session.commit()
        return jsonify({'msg': '课程创建成功！', 'success': True}), 201
        
    except Exception as e:
        db.session.rollback()
        # 打印详细错误信息到控制台
        print(f"Error creating course: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'创建失败: {str(e)}', 'success': False}), 500

# 教师批量导入学生到课程
@course_bp.route('/courses/teacher/import-students', methods=['POST'])
def import_students():
    teacher_id = session.get('user_id')
    if not teacher_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    course_id = request.form.get('course_id')
    if not course_id:
        return jsonify({'msg': '课程ID缺失', 'success': False}), 400
    
    # 验证课程存在且属于该教师
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'msg': '课程不存在', 'success': False}), 404
    if course.teacher_id != teacher_id:
        return jsonify({'msg': '您没有权限操作此课程', 'success': False}), 403
    
    # 获取上传的CSV文件
    if 'csv_file' not in request.files:
        return jsonify({'msg': '未上传文件', 'success': False}), 400
    
    file = request.files['csv_file']
    if file.filename == '':
        return jsonify({'msg': '未选择文件', 'success': False}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'msg': '只支持CSV格式文件', 'success': False}), 400
    
    # 读取CSV文件
    try:
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        
        # 检查列名
        fieldnames = csv_reader.fieldnames
        student_id_column = None
        for field in ['student_id', 'id', 'Student_ID', 'ID', 'StudentID']:
            if field in fieldnames:
                student_id_column = field
                break
        
        if not student_id_column:
            return jsonify({'msg': 'CSV文件必须包含student_id或id列', 'success': False}), 400
        
        # 统计变量
        imported = 0
        failed = 0
        error_details = []
        
        # 当前已选人数
        current_enrolled = CourseEnrollment.query.filter_by(course_id=course_id).count()
        
        for row in csv_reader:
            student_id_str = row.get(student_id_column, '').strip()
            if not student_id_str:
                continue
            
            try:
                student_id = int(student_id_str)
            except ValueError:
                failed += 1
                error_details.append(f'ID {student_id_str} 格式错误')
                continue
            
            # 检查学生是否存在且角色为student
            student = User.query.filter_by(id=student_id, role='student').first()
            if not student:
                failed += 1
                error_details.append(f'学生ID {student_id} 不存在')
                continue
            
            # 检查是否已选该课程
            existing = CourseEnrollment.query.filter_by(
                course_id=course_id, 
                student_id=student_id
            ).first()
            if existing:
                failed += 1
                error_details.append(f'学生ID {student_id} 已选该课程')
                continue
            
            # 检查课程容量
            if current_enrolled >= course.capacity:
                failed += 1
                error_details.append(f'学生ID {student_id} 导入失败：课程已满')
                continue
            
            # 添加选课记录
            new_enrollment = CourseEnrollment(
                course_id=course_id,
                student_id=student_id
            )
            db.session.add(new_enrollment)
            current_enrolled += 1
            imported += 1
        
        db.session.commit()
        
        # 生成详细信息
        details = ''
        if error_details and len(error_details) <= 10:
            details = '失败详情: ' + '; '.join(error_details)
        elif len(error_details) > 10:
            details = f'失败详情(前10条): ' + '; '.join(error_details[:10])
        
        return jsonify({
            'msg': '批量导入完成',
            'success': True,
            'imported': imported,
            'failed': failed,
            'details': details
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'导入失败: {str(e)}', 'success': False}), 500

