# Check available users
from app import app, db
from models import User

with app.app_context():
    users = User.query.all()
    print('Available users:')
    for u in users:
        print(f'  {u.username} - {u.role}')