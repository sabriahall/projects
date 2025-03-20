# security/encryption.py
from cryptography.fernet import Fernet

# NOTE: In a real-world application, generate the key once and store it securely.
# For this project, you can generate a key and save it in a file or environment variable.
def generate_key() -> bytes:
    """
    Generates a new encryption key.
    """
    return Fernet.generate_key()

# For demonstration purposes, we create a cipher_suite with a fixed key.
# You can replace 'your-secret-key' with a securely stored key.
# To generate a key, run: key = generate_key(); print(key)
key = b'8B4uFHrRas7fnpmbRjTkfBI5shHRbVKuuY8zXbbkAL4='  # Replace with a valid 32-byte key
cipher_suite = Fernet(key)

def encrypt_data(plain_text: str) -> bytes:
    """
    Encrypts the provided plain text data.
    """
    return cipher_suite.encrypt(plain_text.encode('utf-8'))

def decrypt_data(encrypted_data: bytes) -> str:
    """
    Decrypts the provided encrypted data.
    """
    return cipher_suite.decrypt(encrypted_data).decode('utf-8')
