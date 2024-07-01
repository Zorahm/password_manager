import logging
from cryptography.fernet import Fernet

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_key():
    """
    Generates a key for encryption and decryption
    """
    key = Fernet.generate_key()
    try:
        with open("decryption_key.key", "wb") as key_file:
            key_file.write(key)
        logging.info("Key generated and saved successfully.")
    except Exception as e:
        logging.error(f"Error generating or saving key: {e}")
    return key

def encrypt_password(password, key):
    """
    Encrypts the given password using the provided key
    """
    f = Fernet(key)
    try:
        encrypted_password = f.encrypt(password.encode())
        logging.info("Password encrypted successfully.")
    except Exception as e:
        logging.error(f"Error encrypting password: {e}")
        raise e
    return encrypted_password

def decrypt_password(encrypted_password, key):
    """
    Decrypts the given password using the provided key
    """
    f = Fernet(key)
    try:
        decrypted_password = f.decrypt(encrypted_password).decode()
        logging.info("Password decrypted successfully.")
    except Exception as e:
        logging.error(f"Error decrypting password: {e}")
        raise e
    return decrypted_password

def save_encrypted_passwords(passwords, filename, key):
    try:
        with open(filename, 'wb') as file:
            for password in passwords:
                encrypted_password = encrypt_password(password, key)
                file.write(encrypted_password + b'\n')
        logging.info("Encrypted passwords saved successfully.")
    except Exception as e:
        logging.error(f"Error saving encrypted passwords: {e}")
        raise e

def read_encrypted_passwords(filename, key):
    try:
        with open(filename, 'rb') as file:
            encrypted_passwords = file.read().splitlines()
            passwords = [decrypt_password(ep, key) for ep in encrypted_passwords]
        logging.info("Encrypted passwords read and decrypted successfully.")
    except Exception as e:
        logging.error(f"Error reading or decrypting passwords: {e}")
        raise e
    return passwords
