from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator

from application.users.exceptions import MismatchPasswordError
from application.users.validators import validate_password


class SignUpIn(BaseModel):
    email: EmailStr
    password1: str = Field(
        ...,
        description="Password must contain min. 8 symbols at least one letter, one number, and one special character.",
        min_length=8,
    )
    password2: str
    first_name: str = Field(..., min_length=1, max_length=70)
    last_name: str = Field(..., min_length=1, max_length=70)

    @field_validator("password1")
    @classmethod
    def validate_password_requirements(cls, password: str) -> str:
        validate_password(password)
        return password

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "SignUpIn":
        if (
            self.password1 is not None
            and self.password2 is not None
            and self.password1 != self.password2
        ):
            raise MismatchPasswordError()
        return self


class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str


class SingIn(BaseModel):
    email: EmailStr
    password: str


class UpdateUserIn(BaseModel):
    first_name: str | None = Field(None, min_length=1, max_length=70)
    last_name: str | None = Field(None, min_length=1, max_length=70)


class SignUpOut(BaseModel):
    user: UserOut
    access_token: str
    refresh_token: str


class SignInOut(SignUpOut): ...


class RefreshTokenIn(BaseModel):
    refresh_token: str


class RefreshTokenOut(BaseModel):
    access_token: str


class ChangePasswordIn(BaseModel):
    old_password: str
    new_password1: str = Field(
        ...,
        description="Password must contain min. 8 symbols at least one letter, one number, and one special character.",
        min_length=8,
    )
    new_password2: str = Field(..., min_length=8)

    @field_validator("new_password1")
    @classmethod
    def validate_password_requirements(cls, password: str) -> str:
        validate_password(password)
        return password

    @model_validator(mode="after")
    def validate_passwords_match(self) -> "ChangePasswordIn":
        if (
            self.new_password1 is not None
            and self.new_password2 is not None
            and self.new_password1 != self.new_password2
        ):
            raise MismatchPasswordError()
        return self


class ChangePasswordOut(BaseModel):
    detail: str
