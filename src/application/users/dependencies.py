from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from application.users.exceptions import AuthenticationError
from application.users.models import User
from application.users.repositories import UserRepository
from application.users.utils import decode_token

oauth2_scheme = HTTPBearer()


async def get_current_user(
    token_data: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> User:
    token = token_data.credentials

    payload = decode_token(token)

    if payload.get("token_type") != "access_token":
        raise AuthenticationError("Not an access token type provided")

    user_id = payload.get("user_id")
    if user_id is None:
        raise AuthenticationError("Token is invalid")

    repository = UserRepository()
    user = await repository.retrieve(user_id)

    if user is None:
        raise AuthenticationError("User not found")

    return user
