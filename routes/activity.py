from flask import Blueprint, request, jsonify, session
from models.activity import Activity
from models.course import Course
from models.user import User, db
import os
import json
import requests
from datetime import datetime, timezone, timedelta

activity_bp = Blueprint('activity', __name__)

# 香港时区 (UTC+8)
HK_TZ = timezone(timedelta(hours=8))

def to_hk_time(dt):
    """将UTC时间转换为香港时间"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        # 假设数据库存储的是UTC时间
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(HK_TZ).isoformat()

# 创建活动
@activity_bp.route('/activities/create', methods=['POST'])
def create_activity():
    teacher_id = session.get('user_id')
    if not teacher_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    try:
        data = request.json
        course_id = data.get('course_id')
        activity_type = data.get('type')
        title = data.get('title')
        description = data.get('description', '')
        content = data.get('content', {})
        
        # 验证必填字段
        if not all([course_id, activity_type, title]):
            return jsonify({'msg': '请填写所有必填字段', 'success': False}), 400
        
        # 验证课程存在且属于该教师
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'msg': '课程不存在', 'success': False}), 404
        
        if course.teacher_id != teacher_id:
            return jsonify({'msg': '您没有权限为此课程创建活动', 'success': False}), 403
        
        # 验证活动类型
        valid_types = ['poll', 'quiz', 'wordcloud', 'short_answer', 'game']
        if activity_type not in valid_types:
            return jsonify({'msg': '无效的活动类型', 'success': False}), 400
        
        # 创建活动
        new_activity = Activity(
            course_id=course_id,
            type=activity_type,
            title=title,
            content=content
        )
        
        db.session.add(new_activity)
        db.session.commit()
        
        return jsonify({
            'msg': '活动创建成功！',
            'success': True,
            'activity_id': new_activity.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating activity: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'创建失败: {str(e)}', 'success': False}), 500

# 获取某个课程的所有活动
@activity_bp.route('/activities/course/<int:course_id>', methods=['GET'])
def get_course_activities(course_id):
    teacher_id = session.get('user_id')
    if not teacher_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    # 验证课程存在且属于该教师
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'msg': '课程不存在', 'success': False}), 404
    
    if course.teacher_id != teacher_id:
        return jsonify({'msg': '您没有权限查看此课程的活动', 'success': False}), 403
    
    # 获取该课程的所有活动
    activities = Activity.query.filter_by(course_id=course_id).order_by(Activity.created_at.desc()).all()
    
    from models.submission import Submission
    result = []
    for a in activities:
        # 统计提交数
        submission_count = Submission.query.filter_by(activity_id=a.id).count()
        
        result.append({
            'id': a.id,
            'title': a.title,
            'type': a.type,
            'content': a.content,
            'created_at': to_hk_time(a.created_at),
            'submission_count': submission_count
        })
    
    return jsonify(result), 200

# 获取单个活动详情
@activity_bp.route('/activities/<int:activity_id>', methods=['GET'])
def get_activity_detail(activity_id):
    teacher_id = session.get('user_id')
    if not teacher_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'msg': '活动不存在', 'success': False}), 404
    
    # 验证权限
    course = Course.query.get(activity.course_id)
    if course.teacher_id != teacher_id:
        return jsonify({'msg': '您没有权限查看此活动', 'success': False}), 403
    
    return jsonify({
        'id': activity.id,
        'course_id': activity.course_id,
        'title': activity.title,
        'type': activity.type,
        'content': activity.content,
        'created_at': to_hk_time(activity.created_at)
    }), 200

# 删除活动
@activity_bp.route('/activities/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    teacher_id = session.get('user_id')
    if not teacher_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'msg': '活动不存在', 'success': False}), 404
    
    # 验证权限
    course = Course.query.get(activity.course_id)
    if course.teacher_id != teacher_id:
        return jsonify({'msg': '您没有权限删除此活动', 'success': False}), 403
    
    try:
        db.session.delete(activity)
        db.session.commit()
        return jsonify({'msg': '活动已删除', 'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': f'删除失败: {str(e)}', 'success': False}), 500

# 学生查看课程活动列表
@activity_bp.route('/activities/student/course/<int:course_id>', methods=['GET'])
def get_student_course_activities(course_id):
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    # 验证学生是否选修了该课程
    from models.course_enrollment import CourseEnrollment
    enrollment = CourseEnrollment.query.filter_by(
        student_id=student_id,
        course_id=course_id
    ).first()
    
    if not enrollment:
        return jsonify({'msg': '您未选修此课程', 'success': False}), 403
    
    # 获取该课程的所有活动
    activities = Activity.query.filter_by(course_id=course_id).order_by(Activity.created_at.desc()).all()
    
    result = []
    for a in activities:
        result.append({
            'id': a.id,
            'title': a.title,
            'type': a.type,
            'created_at': to_hk_time(a.created_at)
        })
    
    return jsonify(result), 200


# AI生成活动内容
@activity_bp.route('/activities/generate-ai', methods=['POST'])
def generate_activity_with_ai():
    teacher_id = session.get('user_id')
    print(f"AI Generate - teacher_id from session: {teacher_id}")
    
    if not teacher_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    try:
        data = request.json
        print(f"AI Generate - request data: {data}")
        
        course_id = data.get('course_id')
        activity_type = data.get('activity_type')
        title = data.get('title')
        teaching_content = data.get('teaching_content')
        requirements = data.get('requirements', '')
        item_count = data.get('item_count', 5)
        difficulty = data.get('difficulty', 'medium')
        
        # 确保course_id是整数
        try:
            course_id = int(course_id)
            print(f"AI Generate - course_id converted to int: {course_id}")
        except (TypeError, ValueError) as e:
            print(f"AI Generate - course_id conversion error: {e}, value: {course_id}")
            return jsonify({'msg': '无效的课程ID', 'success': False}), 400
        
        # 验证课程权限
        course = Course.query.get(course_id)
        if not course:
            print(f"AI Generate - course not found: {course_id}")
            return jsonify({'msg': '课程不存在', 'success': False}), 404
        
        print(f"AI Generate - course found: id={course.id}, teacher_id={course.teacher_id}")
        print(f"AI Generate - comparing: course.teacher_id={course.teacher_id} ({type(course.teacher_id)}), teacher_id={teacher_id} ({type(teacher_id)})")
        
        # 确保类型一致再比较
        if int(course.teacher_id) != int(teacher_id):
            print(f"AI Generate - Permission denied: course.teacher_id={course.teacher_id}, teacher_id={teacher_id}")
            return jsonify({'msg': f'无权限访问此课程 (课程教师ID: {course.teacher_id}, 当前用户ID: {teacher_id})', 'success': False}), 403
        
        # 获取GitHub Token
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            return jsonify({'msg': 'GitHub Token未配置', 'success': False}), 500
        
        # 构建AI提示词
        prompt = build_ai_prompt(activity_type, title, teaching_content, requirements, 
                                 item_count, difficulty, course.name)
        
        # 调用GitHub Models API (使用GPT-4o)
        ai_response = call_github_ai(prompt, github_token)
        
        if ai_response:
            # 解析AI响应并格式化
            content = parse_ai_response(ai_response, activity_type, title)
            return jsonify({
                'msg': 'AI生成成功',
                'success': True,
                'content': content
            }), 200
        else:
            return jsonify({'msg': 'AI生成失败', 'success': False}), 500
            
    except Exception as e:
        print(f"Error generating AI activity: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'生成失败: {str(e)}', 'success': False}), 500

# 构建AI提示词
def build_ai_prompt(activity_type, title, teaching_content, requirements, item_count, difficulty, course_name):
    difficulty_map = {'easy': '简单', 'medium': '中等', 'hard': '困难'}
    
    base_prompt = f"""你是一位经验丰富的教育工作者。请为课程"{course_name}"生成一个{activity_type}类型的教学活动。

活动标题: {title}
教学内容: {teaching_content}
难度级别: {difficulty_map.get(difficulty, '中等')}
"""
    
    if requirements:
        base_prompt += f"额外要求: {requirements}\n"
    
    if activity_type == 'poll':
        base_prompt += f"""
请生成一个投票活动，包含：
1. 一个清晰的投票问题
2. 4-6个选项
3. 简短的活动描述

请以JSON格式返回，格式如下：
{{
    "title": "活动标题",
    "description": "活动描述",
    "question": "投票问题",
    "options": ["选项1", "选项2", "选项3", "选项4"]
}}"""
    
    elif activity_type == 'quiz':
        base_prompt += f"""
请生成{item_count}道选择题，每题包含：
1. 题目问题
2. 4个选项（A、B、C、D）
3. 正确答案的索引（0-3）
4. 简短解释

请以JSON格式返回，格式如下：
{{
    "title": "活动标题",
    "description": "活动描述",
    "questions": [
        {{
            "question": "题目内容",
            "options": ["选项A", "选项B", "选项C", "选项D"],
            "correct_answer": 0,
            "explanation": "答案解释"
        }}
    ]
}}"""
    
    elif activity_type == 'wordcloud':
        base_prompt += f"""
请生成一个词云活动，包含：
1. 引导性问题
2. 建议的最大词数限制（1-5）
3. 活动说明

请以JSON格式返回，格式如下：
{{
    "title": "活动标题",
    "description": "活动描述",
    "question": "引导性问题",
    "maxWords": 3
}}"""
    
    elif activity_type == 'short_answer':
        base_prompt += f"""
请生成一个简答题活动，包含：
1. 开放性问题
2. 参考答案要点（3-5个要点）
3. 建议字数限制

请以JSON格式返回，格式如下：
{{
    "title": "活动标题",
    "description": "活动描述",
    "question": "问题内容",
    "sample_answer": ["要点1", "要点2", "要点3"],
    "maxLength": 500
}}"""
    
    elif activity_type == 'game':
        base_prompt += f"""
请生成{item_count}道选择题用于Monkey Banana游戏，每题包含：
1. 题目问题（与课程内容相关）
2. 4个选项（A、B、C、D）
3. 正确答案的索引（0-3）

请以JSON格式返回，格式如下：
{{
    "title": "活动标题",
    "description": "活动描述",
    "questions": [
        {{
            "question": "题目内容",
            "options": ["选项A", "选项B", "选项C", "选项D"],
            "correct_answer": 0
        }}
    ]
}}"""
    
    base_prompt += "\n\n请确保返回的是纯JSON格式，不要包含任何其他文字说明。"
    return base_prompt

# 调用GitHub Models API
def call_github_ai(prompt, github_token):
    try:
        # GitHub Models API endpoint
        endpoint = "https://models.inference.ai.azure.com/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {github_token}"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "你是一位专业的教育内容生成助手，擅长创建各种类型的教学活动。请始终以JSON格式返回结果。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "gpt-4o",
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            return content
        else:
            print(f"GitHub AI API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error calling GitHub AI: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

# 解析AI响应
def parse_ai_response(ai_response, activity_type, title):
    try:
        # 尝试提取JSON内容
        content = ai_response.strip()
        
        # 移除可能的markdown代码块标记
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        
        content = content.strip()
        
        # 解析JSON
        parsed = json.loads(content)
        
        # 确保包含必要字段
        if 'title' not in parsed:
            parsed['title'] = title
        
        return parsed
        
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {str(e)}")
        print(f"AI Response: {ai_response}")
        # 返回一个默认结构
        return {
            'title': title,
            'description': 'AI生成的内容',
            'error': 'JSON解析失败，请重新生成'
        }

# 学生查看活动详情
@activity_bp.route('/activities/student/<int:activity_id>', methods=['GET'])
def get_student_activity_detail(activity_id):
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'msg': '活动不存在', 'success': False}), 404
    
    # 验证学生是否选修了该课程
    from models.course_enrollment import CourseEnrollment
    enrollment = CourseEnrollment.query.filter_by(
        student_id=student_id,
        course_id=activity.course_id
    ).first()
    
    if not enrollment:
        return jsonify({'msg': '您未选修此课程', 'success': False}), 403
    
    # 解析content JSON
    import json
    content = json.loads(activity.content) if isinstance(activity.content, str) else activity.content
    
    return jsonify({
        'id': activity.id,
        'title': activity.title,
        'type': activity.type,
        'content': content,
        'created_at': to_hk_time(activity.created_at)
    }), 200

# 学生提交活动答案
@activity_bp.route('/activities/submit', methods=['POST'])
def submit_activity():
    print("="*80)
    print("SUBMIT FUNCTION CALLED!")
    print("="*80)
    
    student_id = session.get('user_id')
    print(f"Submit - user_id from session: {student_id}")
    
    if not student_id:
        print("Submit - No user_id in session")
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    # 验证用户角色必须是学生
    user = User.query.get(student_id)
    print(f"Submit - user found: {user.username if user else 'None'}, role: {user.role if user else 'None'}")
    
    if not user:
        print(f"Submit - User not found with id: {student_id}")
        return jsonify({'msg': '用户不存在', 'success': False}), 403
    
    # 暂时注释掉角色检查，方便调试
    # if user.role != 'student':
    #     print(f"Submit - Permission denied: user is {user.role}, not student")
    #     return jsonify({'msg': f'只有学生可以提交活动，当前角色为：{user.role}', 'success': False}), 403
    
    data = request.get_json()
    activity_id = data.get('activity_id')
    answer = data.get('answer')
    
    if not activity_id or not answer:
        return jsonify({'msg': '缺少活动ID或答案', 'success': False}), 400
    
    # 验证活动是否存在
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'msg': '活动不存在', 'success': False}), 404
    
    # 验证学生是否选修了该课程
    from models.course_enrollment import CourseEnrollment
    enrollment = CourseEnrollment.query.filter_by(
        student_id=student_id,
        course_id=activity.course_id
    ).first()
    
    if not enrollment:
        return jsonify({'msg': '您未选修此课程', 'success': False}), 403
    
    try:
        # 解析活动内容
        import json
        content = json.loads(activity.content) if isinstance(activity.content, str) else activity.content
        
        # 自动评分逻辑
        score = None
        is_correct = None
        status = 'submitted'
        
        # Quiz类型：自动评分
        if activity.type == 'quiz' and 'questions' in content:
            correct_count = 0
            total_questions = len(content['questions'])
            student_answers = answer.get('answers', [])
            
            for i, question in enumerate(content['questions']):
                if i < len(student_answers):
                    correct_answer = question.get('correct_answer', question.get('correctAnswer'))
                    if student_answers[i] == correct_answer:
                        correct_count += 1
            
            score = (correct_count / total_questions * 100) if total_questions > 0 else 0
            is_correct = (correct_count == total_questions)
            status = 'graded'
        
        # Poll类型：记录选择，无需评分
        elif activity.type == 'poll':
            status = 'submitted'
            score = None
        
        # 其他类型：等待教师评分
        else:
            status = 'in_review'
        
        # 检查是否已提交过
        from models.submission import Submission
        existing = Submission.query.filter_by(
            activity_id=activity_id,
            student_id=student_id
        ).first()
        
        answer_json = json.dumps(answer, ensure_ascii=False)
        
        if existing:
            # 更新已有提交
            existing.answer = answer_json
            existing.answer_raw = answer_json
            existing.submitted_at = datetime.now(timezone.utc)
            existing.score = score
            existing.is_correct = is_correct
            existing.status = status
            if status == 'graded':
                existing.graded_at = datetime.now(timezone.utc)
        else:
            # 创建新提交
            submission = Submission(
                activity_id=activity_id,
                student_id=student_id,
                answer=answer_json,
                answer_raw=answer_json,
                score=score,
                is_correct=is_correct,
                status=status,
                submitted_at=datetime.now(timezone.utc),
                graded_at=datetime.now(timezone.utc) if status == 'graded' else None
            )
            db.session.add(submission)
        
        db.session.commit()
        
        result = {'msg': '提交成功', 'success': True}
        if score is not None:
            result['score'] = round(score, 2)
            result['status'] = status
        
        return jsonify(result), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Submit error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'提交失败: {str(e)}', 'success': False}), 500

# 教师查看活动的所有提交记录
@activity_bp.route('/activities/<int:activity_id>/submissions', methods=['GET'])
def get_activity_submissions(activity_id):
    teacher_id = session.get('user_id')
    if not teacher_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    # 验证活动是否存在
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'msg': '活动不存在', 'success': False}), 404
    
    # 验证教师权限
    course = Course.query.get(activity.course_id)
    if not course or course.teacher_id != teacher_id:
        return jsonify({'msg': '无权限查看', 'success': False}), 403
    
    try:
        from models.submission import Submission
        submissions = Submission.query.filter_by(activity_id=activity_id).order_by(Submission.submitted_at.desc()).all()
        
        result = []
        for sub in submissions:
            student = User.query.get(sub.student_id)
            import json
            answer_data = json.loads(sub.answer) if isinstance(sub.answer, str) else sub.answer
            
            result.append({
                'id': sub.id,
                'student_id': sub.student_id,
                'student_name': student.username if student else 'Unknown',
                'answer': answer_data,
                'score': sub.score,
                'is_correct': sub.is_correct,
                'status': sub.status,
                'feedback': sub.feedback,
                'submitted_at': to_hk_time(sub.submitted_at),
                'graded_at': to_hk_time(sub.graded_at) if sub.graded_at else None
            })
        
        return jsonify({
            'success': True,
            'activity': {
                'id': activity.id,
                'title': activity.title,
                'type': activity.type
            },
            'submissions': result,
            'total': len(result)
        }), 200
        
    except Exception as e:
        print(f"Get submissions error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'获取失败: {str(e)}', 'success': False}), 500

# 学生查看自己的提交记录
@activity_bp.route('/activities/<int:activity_id>/my-submission', methods=['GET'])
def get_my_submission(activity_id):
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    # 验证活动是否存在
    activity = Activity.query.get(activity_id)
    if not activity:
        return jsonify({'msg': '活动不存在', 'success': False}), 404
    
    # 验证学生是否选修了该课程
    from models.course_enrollment import CourseEnrollment
    enrollment = CourseEnrollment.query.filter_by(
        student_id=student_id,
        course_id=activity.course_id
    ).first()
    
    if not enrollment:
        return jsonify({'msg': '您未选修此课程', 'success': False}), 403
    
    try:
        from models.submission import Submission
        submission = Submission.query.filter_by(
            activity_id=activity_id,
            student_id=student_id
        ).first()
        
        if not submission:
            return jsonify({'success': True, 'submitted': False}), 200
        
        import json
        answer_data = json.loads(submission.answer) if isinstance(submission.answer, str) else submission.answer
        
        result = {
            'success': True,
            'submitted': True,
            'submission': {
                'id': submission.id,
                'answer': answer_data,
                'score': submission.score,
                'is_correct': submission.is_correct,
                'status': submission.status,
                'feedback': submission.feedback,
                'submitted_at': to_hk_time(submission.submitted_at),
                'graded_at': to_hk_time(submission.graded_at) if submission.graded_at else None
            }
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Get my submission error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'获取失败: {str(e)}', 'success': False}), 500

# 教师对提交进行评分和反馈
@activity_bp.route('/submissions/<int:submission_id>/grade', methods=['POST'])
def grade_submission(submission_id):
    teacher_id = session.get('user_id')
    if not teacher_id:
        return jsonify({'msg': '未登录', 'success': False}), 401
    
    data = request.get_json()
    score = data.get('score')
    feedback = data.get('feedback', '')
    
    try:
        from models.submission import Submission
        submission = Submission.query.get(submission_id)
        if not submission:
            return jsonify({'msg': '提交记录不存在', 'success': False}), 404
        
        # 验证教师权限
        activity = Activity.query.get(submission.activity_id)
        course = Course.query.get(activity.course_id)
        if not course or course.teacher_id != teacher_id:
            return jsonify({'msg': '无权限评分', 'success': False}), 403
        
        # 更新评分信息
        submission.score = score
        submission.feedback = feedback
        submission.status = 'graded'
        submission.graded_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        return jsonify({'msg': '评分成功', 'success': True}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Grade error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'评分失败: {str(e)}', 'success': False}), 500

# Get dashboard statistics for student
@activity_bp.route('/activities/statistics', methods=['GET'])
def get_activity_statistics():
    student_id = session.get('user_id')
    if not student_id:
        return jsonify({'msg': 'Not logged in', 'success': False}), 401
    
    try:
        from models.submission import Submission
        from models.course_enrollment import CourseEnrollment
        
        # Get all courses the student is enrolled in
        enrolled_courses = CourseEnrollment.query.filter_by(student_id=student_id).all()
        course_ids = [ec.course_id for ec in enrolled_courses]
        
        if not course_ids:
            return jsonify({'success': True, 'completed': 0, 'incomplete': 0}), 200
        
        # Get all activities from enrolled courses
        all_activities = Activity.query.filter(Activity.course_id.in_(course_ids)).all()
        activity_ids = [a.id for a in all_activities]
        
        # Get student's submissions
        submissions = Submission.query.filter(
            Submission.student_id == student_id,
            Submission.activity_id.in_(activity_ids)
        ).all()
        
        submitted_activity_ids = set(s.activity_id for s in submissions)
        
        completed = len(submitted_activity_ids)
        incomplete = len(activity_ids) - completed
        
        return jsonify({
            'success': True,
            'completed': completed,
            'incomplete': incomplete,
            'total': len(activity_ids)
        }), 200
        
    except Exception as e:
        print(f"Statistics error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'Failed to get statistics: {str(e)}', 'success': False}), 500

        
    except Exception as e:
        db.session.rollback()
        print(f"Submit error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'msg': f'提交失败: {str(e)}', 'success': False}), 500

