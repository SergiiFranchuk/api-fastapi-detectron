from fastapi import HTTPException, status

from users.repositories import UserRepository
from users.schemas import SignIn
from users.utils import hash_password, generate_jwt, validate_password


class BaseUserUseCase:
    accounts = UserRepository()

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError


class UserSignUpUseCase(BaseUserUseCase):

    async def __call__(self, user_data: dict):
        if await self.accounts.retrieve_by_email(user_data.get("email")):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="email already in use"
            )
        user_data["password"] = hash_password(user_data.get("password"))
        user = await self.accounts.create(user_data)

        token = generate_jwt(user)

        return {"user": user, "access_token": token}


class UserSignInUseCase(BaseUserUseCase):

    async def __call__(self, credentials: dict):
        authentication_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )
        user = await self.accounts.retrieve_by_email(credentials.get("email"))

        if not user or not validate_password(credentials.get("email"), user.password):
            raise authentication_exception

        token = generate_jwt(user)

        return {"access_token": token, "token_type": "Bearer"}
