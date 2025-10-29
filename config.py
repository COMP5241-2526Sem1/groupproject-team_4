import os

class Config:
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://root:root@localhost/learning_platform'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Optionally, use environment variables to manage username and password
# class Config:
#     SQLALCHEMY_DATABASE_URI = (
#         f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@localhost/learning_platform"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
