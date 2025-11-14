from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Find alice_johnson user
    user = User.query.filter_by(username='alice_johnson').first()
    if user:
        print(f"User found: {user.username}")
        print(f"Role: {user.role}")
        print(f"Email: {user.email}")
        
        # Try to check if password is 'password123'
        from werkzeug.security import check_password_hash
        if check_password_hash(user.password_hash, 'password123'):
            print("Password 'password123' is correct")
        else:
            print("Password 'password123' is incorrect")
            
        # Try other common passwords
        common_passwords = ['alice123', 'alice_johnson123', 'student123', '123456']
        for pwd in common_passwords:
            if check_password_hash(user.password_hash, pwd):
                print(f"Password '{pwd}' is correct")
                break
        else:
            print("None of the common passwords worked")
            
        # Let's also check what users we have
        print("\nAll users:")
        users = User.query.all()
        for u in users:
            print(f"  {u.username} ({u.role})")
    else:
        print("alice_johnson not found")
        
        # Let's see what users we have
        print("Available users:")
        users = User.query.all()
        for u in users:
            print(f"  {u.username} ({u.role})")