from datetime import datetime, timedelta

import bcrypt
import jwt

from application import settings
from application.users.exceptions import AuthenticationError
from application.users.models import User


def generate_jwt(user: User, lifetime: timedelta, refresh_token: bool = False) -> str:
    token_type = "access"

    if refresh_token:
        token_type = "refresh"

    now = datetime.utcnow()
    expire = now + lifetime

    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": expire,
        "token_type": token_type,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        raise AuthenticationError("Invalid or expired token")
    return payload


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)
