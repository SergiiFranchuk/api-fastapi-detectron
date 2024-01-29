from datetime import datetime, timedelta
from hashlib import sha256

import jwt

import settings
from users.models import User


def generate_jwt(user: User) -> str:

    now = datetime.utcnow()
    expire = now + timedelta(seconds=settings.TOKEN_EXPIRED_TIME)

    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def hash_password(password):
    sha256().update(password.encode("utf-8"))
    hashed_password = sha256().digest().hex()
    return hashed_password


def validate_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password
