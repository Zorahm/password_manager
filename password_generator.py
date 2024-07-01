import random
import string


def generate_password(length, include_uppercase=True, include_numbers=True, include_special=True, template=None,
                      exclude_chars=""):
    if template:
        characters = template
    else:
        characters = string.ascii_lowercase
        if include_uppercase:
            characters += string.ascii_uppercase
        if include_numbers:
            characters += string.digits
        if include_special:
            characters += string.punctuation

    characters = ''.join(c for c in characters if c not in exclude_chars)

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_multiple_passwords(count, length, include_uppercase=True, include_numbers=True, include_special=True,
                                template=None, exclude_chars=""):
    passwords = [generate_password(length, include_uppercase, include_numbers, include_special, template, exclude_chars)
                 for _ in range(count)]
    return passwords
