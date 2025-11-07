from app import app
from database import db
from models.user import User
from werkzeug.security import check_password_hash

with app.app_context():
    user = User.query.filter_by(username='john_smith').first()
    if user:
        # Test simple passwords that might match the hash
        test_passwords = ['password', 'password123', '123456', 'test', 'abc123']
        for pwd in test_passwords:
            if check_password_hash(user.password_hash, pwd):
                print(f"✅ Found password: {pwd}")
                break
        else:
            print("❌ Common passwords didn't work")
            # Let's try to create a new teacher user with known password
            print("Creating new test teacher...")
            from werkzeug.security import generate_password_hash
            new_user = User(
                username='debug_teacher',
                password_hash=generate_password_hash('debug123'),
                role='teacher',
                email='debug@teacher.com'
            )
            db.session.add(new_user)
            db.session.commit()
            print("✅ Created debug_teacher with password: debug123")