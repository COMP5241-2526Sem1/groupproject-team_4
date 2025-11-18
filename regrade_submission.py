"""为现有的提交记录重新评分"""
from app import app
from models import db
from models.submission import Submission
from models.activity import Activity
import json
from datetime import datetime, timezone

def regrade_submission():
    with app.app_context():
        # 获取student1对活动11的提交
        submission = Submission.query.filter_by(activity_id=11, student_id=4).first()
        if not submission:
            print("未找到提交记录")
            return
        
        # 获取活动信息
        activity = Activity.query.get(11)
        content = json.loads(activity.content) if isinstance(activity.content, str) else activity.content
        
        # 获取学生答案
        answer_data = json.loads(submission.answer) if isinstance(submission.answer, str) else submission.answer
        student_answers = answer_data.get('answers', [])
        
        # 重新评分
        correct_count = 0
        total_questions = len(content['questions'])
        
        for i, question in enumerate(content['questions']):
            if i < len(student_answers):
                correct_answer = question.get('correct_answer', question.get('correctAnswer'))
                if student_answers[i] == correct_answer:
                    correct_count += 1
        
        score = (correct_count / total_questions * 100) if total_questions > 0 else 0
        is_correct = (correct_count == total_questions)
        
        print(f"原始数据:")
        print(f"  分数: {submission.score}")
        print(f"  状态: {submission.status}")
        print(f"  是否全对: {submission.is_correct}")
        
        # 更新提交记录
        submission.score = score
        submission.is_correct = is_correct
        submission.status = 'graded'
        submission.graded_at = datetime.now(timezone.utc)
        
        db.session.commit()
        
        print(f"\n更新后数据:")
        print(f"  正确数: {correct_count}/{total_questions}")
        print(f"  分数: {score}")
        print(f"  状态: {submission.status}")
        print(f"  是否全对: {is_correct}")
        print(f"  评分时间: {submission.graded_at}")
        print("\n✅ 评分完成！")

if __name__ == '__main__':
    regrade_submission()
