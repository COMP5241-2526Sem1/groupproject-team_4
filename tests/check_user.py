from app import app
from models.user import User

with app.app_context():
    # Check user 'a' details
    user_a = User.query.filter_by(username='a').first()
    if user_a:
        print(f"User 'a' details:")
        print(f"  Username: {user_a.username}")
        print(f"  Email: {user_a.email}")
        print(f"  Role: {user_a.role}")
        print(f"  Password hash: {user_a.password}")
    else:
        print("User 'a' not found")