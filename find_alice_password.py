from app import app, db
from models.user import User
from werkzeug.security import check_password_hash

with app.app_context():
    # Find alice_johnson user
    user = User.query.filter_by(username='alice_johnson').first()
    if user:
        print(f"alice_johnson ID: {user.id}")
        
        # Find alice's password
        test_passwords = ['password', '123456', 'student', 'alice', 'alice_johnson', 'alice123', 'comp5241']
        for pwd in test_passwords:
            if check_password_hash(user.password_hash, pwd):
                print(f"alice_johnson password: {pwd}")
                break
        else:
            print("Password not found in common list")
    else:
        print("alice_johnson user not found")