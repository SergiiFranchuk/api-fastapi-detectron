from typing import Optional

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from users.exceptions import AuthenticationError
from users.repositories import UserRepository
from users.utils import decode_token

oauth2_scheme = HTTPBearer()


async def get_current_user(
    token_data: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> int:
    token = token_data.credentials

    payload = decode_token(token)

    user_id: Optional[int] = payload.get("user_id")
    if user_id is None:
        raise AuthenticationError("Token is invalid")

    repository = UserRepository()
    user = await repository.retrieve(user_id)

    if user is None:
        raise AuthenticationError("User not found")

    return user
