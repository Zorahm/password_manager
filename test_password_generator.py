import unittest
import os
import string
from password_generator import (
    generate_password, generate_multiple_passwords
)
from encryption_utils import (
    generate_key, encrypt_password, decrypt_password,
    save_encrypted_passwords, read_encrypted_passwords
)

class TestPasswordGenerator(unittest.TestCase):

    def test_generate_password_length(self):
        password = generate_password(10)
        self.assertEqual(len(password), 10)

    def test_generate_password_uppercase(self):
        password = generate_password(10, include_uppercase=True, include_numbers=False, include_special=False)
        self.assertTrue(any(c.isupper() for c in password))

    def test_generate_password_numbers(self):
        password = generate_password(10, include_uppercase=False, include_numbers=True, include_special=False)
        self.assertTrue(any(c.isdigit() for c in password))

    def test_generate_password_special(self):
        password = generate_password(10, include_uppercase=False, include_numbers=False, include_special=True)
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_generate_multiple_passwords(self):
        passwords = generate_multiple_passwords(5, 10)
        self.assertEqual(len(passwords), 5)
        self.assertTrue(all(len(p) == 10 for p in passwords))

    def test_generate_password_with_template(self):
        template = 'abc123'
        password = generate_password(10, template=template)
        self.assertTrue(all(c in template for c in password))

    def test_generate_password_with_excluded_chars(self):
        exclude_chars = 'abc123'
        password = generate_password(10, exclude_chars=exclude_chars)
        self.assertTrue(all(c not in exclude_chars for c in password))

    def test_encryption_decryption(self):
        password = "TestPassword123!"
        key = generate_key()
        encrypted_password = encrypt_password(password, key)
        decrypted_password = decrypt_password(encrypted_password, key)
        self.assertEqual(password, decrypted_password)

    def test_save_and_read_encrypted_passwords(self):
        passwords = generate_multiple_passwords(5, 10)
        filename = 'test_passwords.txt'
        key = generate_key()
        save_encrypted_passwords(passwords, filename, key)
        read_passwords = read_encrypted_passwords(filename, key)
        self.assertEqual(passwords, read_passwords)
        os.remove(filename)  # Clean up

if __name__ == '__main__':
    unittest.main()
