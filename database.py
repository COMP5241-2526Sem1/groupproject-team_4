from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize database object
db = SQLAlchemy()

# Database connection configuration
def init_db(app):
    app.config.from_object(Config)
    db.init_app(app)

# Example: Test database connection
def test_db_connection():
    try:
        with app.app_context():
            db.engine.connect()
            print("数据库连接成功！")
    except Exception as e:
        print(f"数据库连接失败: {e}")