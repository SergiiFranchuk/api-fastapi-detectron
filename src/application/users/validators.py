import re


def validate_password(password: str) -> str:
    if not re.search("[a-zA-Z]", password):
        raise ValueError("Password must contain at least one letter")
    if not re.search("[0-9]", password):
        raise ValueError("Password must contain at least one number")
    if not re.search('[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("Password must contain at least one special character")
    return password
