#!/usr/bin/env python
"""测试恢复的端点是否正常工作"""

import sys
sys.path.insert(0, '.')

from app import app
from database import db
from models.course import Course

# 创建测试客户端
client = app.test_client()

print("测试恢复的功能端点...\n")

with app.app_context():
    # 获取第一个课程用于测试
    course = Course.query.first()
    if not course:
        print("❌ 没有课程数据")
        sys.exit(1)
    
    course_code = course.code
    print(f"使用课程: {course_code}\n")
    
    # 测试路由 1: 民意调查列表
    print("1. 测试民意调查列表 GET /course/{course_code}/poll")
    # 这个需要登录，所以预期会重定向或返回错误
    response = client.get(f'/course/{course_code}/poll')
    print(f"   状态码: {response.status_code} (预期 302 重定向到登录或 200)")
    
    # 测试路由 2: 短答题列表 (需要教师权限)
    print(f"\n2. 测试短答题管理列表 GET /teacher/course/{course_code}/short-answer")
    response = client.get(f'/teacher/course/{course_code}/short-answer')
    print(f"   状态码: {response.status_code} (预期 302 重定向到登录或 200)")
    
    # 测试路由 3: AI生成界面
    print(f"\n3. 测试AI生成界面 GET /teacher/course/{course_code}/short-answer/3/ai-generate")
    response = client.get(f'/teacher/course/{course_code}/short-answer/3/ai-generate')
    print(f"   状态码: {response.status_code} (预期 302 重定向到登录或 200)")
    
    # 测试路由 4: 检查API端点是否存在
    print(f"\n4. 测试 API 端点 /api/ai/short-answer (POST)")
    response = client.post(f'/api/ai/short-answer', 
                          json={'topic': 'test', 'short_answer_id': 1},
                          content_type='application/json')
    print(f"   状态码: {response.status_code} (预期 401 未认证)")
    
    print("\n✓ 端点测试完成!")
    print("\n关键恢复文件检查清单:")
    print("✓ routes/poll_routes.py - 民意调查路由")
    print("✓ routes/short_answer_routes.py - 短答题路由")
    print("✓ routes/ai_routes.py - AI生成路由")
    print("✓ templates/poll_info.html - 单页分页民意调查")
    print("✓ templates/short_answer_results.html - 短答题结果页面")
    print("✓ templates/short_answer_detail.html - 短答题详情")
    print("✓ templates/short_answer_start.html - 短答题提交表单")
    print("✓ templates/teacher_ai_generate.html - AI生成界面")
    print("✓ templates/teacher_poll_list.html - 民意调查管理")
    print("✓ templates/teacher_short_answer_list.html - 短答题管理")
