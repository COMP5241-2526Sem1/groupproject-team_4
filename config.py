import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database configuration
    if os.environ.get('VERCEL'):
        # Use Vercel Postgres connection string
        SQLALCHEMY_DATABASE_URI = os.environ.get('POSTGRES_URL')
    else:
        # Use local PostgreSQL configuration
        try:
            SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('PG_DB_USER')}:{os.getenv('PG_DB_PASSWORD')}@{os.getenv('PG_DB_HOST')}:{os.getenv('PG_DB_PORT')}/{os.getenv('PG_DB_NAME')}"
        except:
            # Fallback to SQLite for development/testing
            SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False