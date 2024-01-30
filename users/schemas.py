from pydantic import BaseModel, EmailStr, Field


class SignUpIn(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str = Field(
        min_length=8,
    )


class UserOut(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str


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
