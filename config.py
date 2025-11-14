import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Database configuration
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('PG_DB_USER')}:{os.getenv('PG_DB_PASSWORD')}@{os.getenv('PG_DB_HOST')}:{os.getenv('PG_DB_PORT')}/{os.getenv('PG_DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False