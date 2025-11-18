import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Config:
    # 使用 Supabase PostgreSQL 数据库
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('PG_DB_USER')}:{os.getenv('PG_DB_PASSWORD')}"
        f"@{os.getenv('PG_DB_HOST')}:{os.getenv('PG_DB_PORT')}/{os.getenv('PG_DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_123456789')
