from typing import Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import settings
from users.exceptions import AuthenticationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="signin")


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: Optional[int] = payload.get("user_id")
        if user_id is None:
            raise AuthenticationError()
    except JWTError as error:
        with open("file.txt", "w") as file:
            file.write(error.args[0])
        raise AuthenticationError(error.args)

    return user_id
