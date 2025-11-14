from app import app
from models import db, User
from werkzeug.security import check_password_hash

with app.app_context():
    # Test all users with common passwords
    users = User.query.all()
    test_passwords = ['password', '123456', 'student', 'teacher', 'debug123']
    
    print("Testing passwords for all users:")
    for user in users:
        found_password = None
        for pwd in test_passwords:
            if check_password_hash(user.password_hash, pwd):
                found_password = pwd
                break
        
        if found_password:
            print(f"  {user.username} ({user.role}): {found_password}")
        else:
            print(f"  {user.username} ({user.role}): Password not found in common list")