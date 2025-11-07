#!/usr/bin/env python3
"""
Debug script to check SQL loading issues
"""

import re
import psycopg2
from database import db
from app import app

def debug_load():
    """Debug the SQL loading process"""
    
    # Read the SQL file
    with open('sample_data_refactored.sql', 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    print("=== Debug SQL Loading ===")
    print(f"SQL file size: {len(sql_content)} characters")
    
    # Split statements
    statements = re.split(r';\s*$', sql_content, flags=re.MULTILINE)
    statements = [stmt.strip() for stmt in statements if stmt.strip()]
    
    print(f"Found {len(statements)} SQL statements")
    
    # Test first few statements
    with app.app_context():
        for i, statement in enumerate(statements[:5]):
            print(f"\nStatement {i+1}:")
            print(f"First 100 chars: {statement[:100]}...")
            
            if statement.strip().startswith('--') or not statement.strip():
                print("Skipping comment/empty")
                continue
                
            try:
                db.session.execute(statement)
                db.session.commit()
                print("✓ Executed successfully")
                
                # Check if it was an INSERT
                if 'INSERT INTO department' in statement:
                    result = db.session.execute("SELECT COUNT(*) FROM department")
                    count = result.fetchone()[0]
                    print(f"Department count after insert: {count}")
                    
            except Exception as e:
                print(f"✗ Error: {e}")
                db.session.rollback()
                break

if __name__ == "__main__":
    debug_load()