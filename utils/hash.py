import bcrypt

def hash_generator(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(hashed, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)