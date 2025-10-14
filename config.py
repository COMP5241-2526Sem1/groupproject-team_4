import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:root@localhost/learning_platform'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# 如果需要，可以用环境变量管理用户名和密码
# class Config:
#     SQLALCHEMY_DATABASE_URI = (
#         f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@localhost/learning_platform"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
