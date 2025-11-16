from werkzeug.security import check_password_hash

# From clean_statements.sql - this is the hash for alice_johnson and others
hash_value = 'scrypt:32768:8:1$Qilrw14F5BEVgyrb$3a38992073b7444d9ead3809e0c285ea1062b578990e1f7b28b79ea652b631743a8ce2ed139cfa9041fa2eafb0c76baa166a917f74e952ab58d74b3b0831af88'

# Test common passwords
test_passwords = ['password', 'password123', '123456', 'student', 'teacher', 'admin', 'comp5241']

print("Testing hash against common passwords:")
for pwd in test_passwords:
    if check_password_hash(hash_value, pwd):
        print(f"✅ Found it! Password is: '{pwd}'")
        break
else:
    print("❌ Password not found in common list")
    
print("Testing some more variations:")
more_passwords = ['alice', 'alice123', 'john', 'smith', 'bob', 'williams', 'carol', 'davis']
for pwd in more_passwords:
    if check_password_hash(hash_value, pwd):
        print(f"✅ Found it! Password is: '{pwd}'")
        break