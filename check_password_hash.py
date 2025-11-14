from app import app
from database import db
from models.user import User

with app.app_context():
    user = User.query.filter_by(username='john_smith').first()
    if user:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Password hash: {user.password_hash}")
        print(f"Password hash length: {len(user.password_hash)}")
        
        # Let's also check other teacher users
        teachers = User.query.filter_by(role='teacher').all()
        print(f"\nAll teachers:")
        for t in teachers:
            print(f"  {t.username}: {t.email}")