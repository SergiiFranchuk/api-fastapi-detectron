from fastapi import Form
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


class SignUpOut(BaseModel):
    user: UserOut
    access_token: str


class SignIn(BaseModel):
    email: EmailStr
    password: str


class SignInOut(BaseModel):
    access_token: str
    token_type: str
