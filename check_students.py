from app import app, db
from models.user import User

with app.app_context():
    # Find all student users
    students = User.query.filter_by(role='student').all()
    print('Available students:')
    for student in students:
        print(f'  Username: {student.username}')
        
    # Also check if there are any debug students
    debug_students = User.query.filter(User.username.like('%debug%student%')).all()
    if debug_students:
        print('Debug students:')
        for student in debug_students:
            print(f'  Username: {student.username}')