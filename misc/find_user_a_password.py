from app import app
from models import db, User
from werkzeug.security import check_password_hash

with app.app_context():
    # Find user 'a' and test common passwords
    user_a = User.query.filter_by(username='a').first()
    
    if user_a:
        print(f"Found user 'a' with password hash: {user_a.password_hash}")
        
        # Test common passwords
        passwords_to_test = ['a', 'password', '123456', 'student', 'teacher', 'debug123', 'comp5241', 'password123']
        
        for password in passwords_to_test:
            if check_password_hash(user_a.password_hash, password):
                print(f"✅ User 'a' password is: {password}")
                break
        else:
            print("❌ Could not find password for user 'a'")
    else:
        print("❌ User 'a' not found")