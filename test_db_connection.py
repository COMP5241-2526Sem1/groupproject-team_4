import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()

# Test PostgreSQL connection
def test_postgresql_connection():
    try:
        # Get PostgreSQL connection details from .env
        PG_DB_HOST = os.getenv("PG_DB_HOST")
        PG_DB_USER = os.getenv("PG_DB_USER")
        PG_DB_PASSWORD = os.getenv("PG_DB_PASSWORD")
        PG_DB_NAME = os.getenv("PG_DB_NAME")
        PG_DB_PORT = os.getenv("PG_DB_PORT")

        # Connect to PostgreSQL using SQLAlchemy
        engine = create_engine(
            f"postgresql://{PG_DB_USER}:{PG_DB_PASSWORD}@{PG_DB_HOST}:{PG_DB_PORT}/{PG_DB_NAME}"
        )
        conn = engine.connect()

        # Execute a simple query
        result = conn.execute(text("SELECT version();"))
        db_version = result.fetchone()
        print(f"PostgreSQL version: {db_version}")

        # Close the connection
        conn.close()
        print("PostgreSQL connection test passed!")
    except Exception as e:
        print(f"PostgreSQL connection test failed: {e}")

# Test MySQL connection
def test_mysql_connection():
    try:
        # Get MySQL connection details from .env
        MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST")
        MYSQL_DB_USER = os.getenv("MYSQL_DB_USER")
        MYSQL_DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD")
        MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME")
        MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT")
        MYSQL_SSL_MODE = os.getenv("MYSQL_SSL_MODE")

        # Connect to MySQL using SQLAlchemy
        engine = create_engine(
            f"mysql+pymysql://{MYSQL_DB_USER}:{MYSQL_DB_PASSWORD}@{MYSQL_DB_HOST}:{MYSQL_DB_PORT}/{MYSQL_DB_NAME}",
            connect_args={"ssl": {"ca": None}} if MYSQL_SSL_MODE == "REQUIRED" else {}
        )
        conn = engine.connect()

        # Execute a simple query
        result = conn.execute(text("SELECT VERSION();"))
        db_version = result.fetchone()
        print(f"MySQL version: {db_version}")

        # Close the connection
        conn.close()
        print("MySQL connection test passed!")
    except Exception as e:
        print(f"MySQL connection test failed: {e}")

if __name__ == "__main__":
    test_postgresql_connection()
    #test_mysql_connection()