from app import app
from database import db
from models.user import User
from werkzeug.security import check_password_hash

with app.app_context():
    user = User.query.filter_by(username='john_smith').first()
    if user:
        print(f"User found: {user.username}, role: {user.role}")
        # Test common passwords
        test_passwords = ['password123', 'password', '123456', 'john', 'smith']
        for pwd in test_passwords:
            if check_password_hash(user.password_hash, pwd):
                print(f"✅ Password is: {pwd}")
                break
        else:
            print("❌ None of the common passwords worked")
    else:
        print("User not found")