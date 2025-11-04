from .course import course_bp  # 导入 course 模块的蓝图
from .auth import auth_bp      # 导入 auth 模块的蓝图

# 定义 __all__ 变量，控制 from routes import * 的行为
__all__ = ['course_bp', 'auth_bp']