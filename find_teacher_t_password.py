from app import app, db
from models.user import User
from werkzeug.security import check_password_hash

with app.app_context():
    # Find teacher 't'
    teacher = User.query.filter_by(username='t').first()
    if teacher:
        print(f'Teacher t ID: {teacher.id}')
        
        # Find teacher's password with more options
        test_passwords = ['password', '123456', 'teacher', 't', 't123', 'debug123', 'password123', 'comp5241', 'test123', 'debug']
        for pwd in test_passwords:
            if check_password_hash(teacher.password_hash, pwd):
                print(f'Teacher t password: {pwd}')
                break
        else:
            print('Password not found in common list')
            
        # Also check if this teacher has email or other identifying info
        print(f'Teacher details: username={teacher.username}, email={teacher.email}, role={teacher.role}')
    else:
        print('Teacher t not found')