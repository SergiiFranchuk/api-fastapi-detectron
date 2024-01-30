from datetime import datetime, timedelta
from hashlib import sha256

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


def hash_password(password):
    sha256().update(password.encode("utf-8"))
    hashed_password = sha256().digest().hex()
    return hashed_password


def validate_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password
