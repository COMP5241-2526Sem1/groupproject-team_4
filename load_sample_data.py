#!/usr/bin/env python3
"""
Script to load sample data from SQL file
"""

from app import app
from database import db
from sqlalchemy import text
import re

def load_sample_data():
    """Load sample data from SQL file"""
    
    with app.app_context():
        try:
            # Read the SQL file
            with open('sample_data_with_ids.sql', 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Split SQL content into individual statements
            # Split by semicolon, but handle cases where semicolon is inside strings
            statements = re.split(r';\s*(?=INSERT|UPDATE|DELETE|--)', sql_content, flags=re.IGNORECASE)
            
            # Execute each statement separately
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--') and not statement.startswith('/*'):
                    # Remove any trailing semicolons and whitespace
                    statement = statement.rstrip(';').strip()
                    if statement:
                        try:
                            db.session.execute(text(statement))
                        except Exception as e:
                            print(f"Error executing statement: {statement[:100]}...")
                            print(f"Error: {e}")
                            raise
            
            db.session.commit()
            print("✓ Sample data loaded successfully")
            
        except Exception as e:
            print(f"✗ Failed to load sample data: {e}")
            db.session.rollback()

if __name__ == "__main__":
    load_sample_data()