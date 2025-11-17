from app import app
from models import db, User
from werkzeug.security import check_password_hash

with app.app_context():
    # Test debug_teacher account
    user = User.query.filter_by(username='debug_teacher').first()
    if user:
        print(f"Found debug_teacher user")
        
        # Test common passwords
        test_passwords = ['debug123', 'password', '123456', 'teacher', 'debug']
        for pwd in test_passwords:
            if check_password_hash(user.password_hash, pwd):
                print(f"Password for debug_teacher is: {pwd}")
                break
        else:
            print("None of the test passwords worked for debug_teacher")
    else:
        print("debug_teacher not found")
        
    # Let's also check what the hash from SQL corresponds to
    # From the clean_statements.sql, the hash is the same for all users
    hash_from_sql = 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88'
    
    # Test alice_johnson with common passwords
    alice = User.query.filter_by(username='alice_johnson').first()
    if alice:
        test_passwords = ['password', '123456', 'student', 'alice', 'alice_johnson']
        for pwd in test_passwords:
            if check_password_hash(alice.password_hash, pwd):
                print(f"Password for alice_johnson is: {pwd}")
                break