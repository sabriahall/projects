# security/auth.py
import bcrypt
import sqlite3

def hash_password(password: str) -> bytes:
    """
    Hash a password for storing.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(stored_hash: bytes, password_attempt: str) -> bool:
    """
    Check if the provided password matches the stored hash.
    """
    return bcrypt.checkpw(password_attempt.encode('utf-8'), s…a parameterized query to get the hashed password for the user
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_hash = result[0]
        # stored_hash might be stored as a string; convert to bytes if necessary
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode('utf-8')
        return verify_password(stored_hash, password)
    else:
        return False