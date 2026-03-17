import re
from passlib.hash import bcrypt


def hash_password(password):

    return bcrypt.hash(password)


def verify_password(password, hashed):

    return bcrypt.verify(password, hashed)


def validate_password(password):

    if len(password) < 8 or len(password) > 16:
        return "Password must be 8–16 characters"

    if not re.search(r"[A-Z]", password):
        return "Password must contain an uppercase letter"

    if not re.search(r"[!@#$%^&*()_+]", password):
        return "Password must contain a special character"

    return None
