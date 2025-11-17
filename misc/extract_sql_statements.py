#!/usr/bin/env python3
"""
Extract clean SQL statements from the file
"""

import re

def extract_sql_statements():
    """Extract clean SQL statements from the SQL file"""
    
    # Read the SQL file
    with open('sample_data_refactored.sql', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove all comments
    # Remove single-line comments
    content = re.sub(r'--.*$', '', content, flags=re.MULTILINE)
    
    # Remove empty lines and extra whitespace
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Join lines back and split by semicolon
    clean_content = ' '.join(lines)
    statements = [stmt.strip() for stmt in clean_content.split(';') if stmt.strip()]
    
    print("=== Extracted SQL Statements ===")
    for i, stmt in enumerate(statements, 1):
        print(f"Statement {i}: {stmt[:100]}...")
    
    # Write clean statements to a new file
    with open('clean_statements.sql', 'w', encoding='utf-8') as f:
        for stmt in statements:
            f.write(stmt + ';\n\n')
    
    print(f"\n✓ Extracted {len(statements)} clean SQL statements to clean_statements.sql")
    return statements

if __name__ == "__main__":
    statements = extract_sql_statements()