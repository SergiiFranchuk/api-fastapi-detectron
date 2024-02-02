from fastapi import HTTPException, status

from application import settings
from application.users.exceptions import AuthenticationError
from application.users.models import User
from application.users.repositories import UserRepository
from application.users.utils import (
    hash_password,
    generate_jwt,
    verify_password,
    decode_token,
)


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

    async def __call__(self, user_data: dict) -> dict:
        if await self.accounts.retrieve_by_email(user_data.get("email")):

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="email already in use"
            )
        user_data["password"] = hash_password(user_data.get("password1"))
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

    async def __call__(self, credentials: dict) -> dict:

        user = await self.accounts.retrieve_by_email(credentials.get("email"))

        if not user or not verify_password(credentials.get("password"), user.password):
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

    async def __call__(self, token) -> dict:
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
    async def __call__(self, payload: dict) -> dict:

        if not verify_password(payload.get("old_password"), self.user.password):
            raise AuthenticationError(
                "Your old password was entered incorrectly. Please enter it again"
            )

        await self.accounts.update(
            self.user.id, {"password": hash_password(payload.get("new_password1"))}
        )
        return {"detail": "New password has been saved."}


class UpdateCurrentUserUseCase(BaseAuthorizedUserUseCase):
    async def __call__(self, payload: dict) -> User:

        await self.accounts.update(self.user.id, {**payload})

        updated_user = await self.accounts.retrieve(self.user.id)

        return updated_user
