from fastapi import HTTPException, status

import settings
from users.exceptions import AuthenticationError
from users.models import User
from users.repositories import UserRepository
from users.utils import hash_password, generate_jwt, validate_password, decode_token


class BaseUnauthorizedUserUseCase:
    def __init__(self):
        self.accounts = UserRepository()

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError


class BaseAuthorizedUserUseCase:
    def __init__(self, user: User):
        self.user = user
        self.accounts = UserRepository()

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError


class UserSignUpUseCase(BaseUnauthorizedUserUseCase):

    async def __call__(self, user_data: dict):
        if await self.accounts.retrieve_by_email(user_data.get("email")):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="email already in use"
            )
        user_data["password"] = hash_password(user_data.get("password"))
        user = await self.accounts.create(user_data)

        return {
            "user": user,
            "access_token": generate_jwt(
                user, lifetime=settings.JWT_ACCESS_TOKEN_LIFETIME
            ),
            "refresh_token": generate_jwt(
                user, lifetime=settings.JWT_REFRESH_TOKEN_LIFETIME, refresh_token=True
            ),
        }


class UserSignInUseCase(BaseUnauthorizedUserUseCase):

    async def __call__(self, email: str, password: str):

        user = await self.accounts.retrieve_by_email(email)

        if not user or not validate_password(password, user.password):
            raise AuthenticationError("invalid username or password")

        return {
            "user": user,
            "access_token": generate_jwt(
                user, lifetime=settings.JWT_ACCESS_TOKEN_LIFETIME
            ),
            "refresh_token": generate_jwt(
                user, lifetime=settings.JWT_REFRESH_TOKEN_LIFETIME, refresh_token=True
            ),
        }


class RefreshAccessTokenUseCase(BaseUnauthorizedUserUseCase):

    async def __call__(self, token):
        payload = decode_token(token)

        if payload.get("token_type") != "refresh_token":
            raise AuthenticationError("Refresh token is invalid")

        user = await self.accounts.retrieve_by_email(payload.get("email"))

        if user is None:
            raise AuthenticationError("Refresh token is invalid")

        return {
            "access_token": generate_jwt(
                user, lifetime=settings.JWT_ACCESS_TOKEN_LIFETIME
            )
        }


class PasswordChangeUseCase(BaseAuthorizedUserUseCase):
    async def __call__(self, old_password: str, new_password):

        if not validate_password(old_password, self.user.password):
            raise AuthenticationError(
                "Your old password was entered incorrectly. Please enter it again"
            )

        await self.accounts.update(
            self.user.id, {"password": hash_password(new_password)}
        )


class UpdateCurrentUserUseCase(BaseAuthorizedUserUseCase):
    async def __call__(self, payload: dict):

        await self.accounts.update(self.user.id, {**payload})

        updated_user = await self.accounts.retrieve(self.user.id)

        return updated_user
