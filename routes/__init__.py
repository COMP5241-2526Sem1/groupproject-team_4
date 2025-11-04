from .course import course_bp  # 导入 course 模块的蓝图
from .auth import auth_bp      # 导入 auth 模块的蓝图
from .quiz_routes import quiz_bp  # 导入 quiz_routes 模块的蓝图
from .poll_routes import poll_bp  # 导入 poll_routes 模块的蓝图
from .course_registration import course_registration_bp  # 导入 course_registration 模块的蓝图

# 定义 __all__ 变量，控制 from routes import * 的行为
__all__ = ['course_bp', 'auth_bp', 'quiz_bp', 'poll_bp', 'course_registration_bp']