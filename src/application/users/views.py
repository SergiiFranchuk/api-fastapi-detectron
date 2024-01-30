from fastapi import APIRouter, Form, status, Depends
from pydantic import EmailStr

from application.users.dependencies import get_current_user
from application.users.models import User
from application.users.schemas import (
    SignUpIn,
    SignUpOut,
    SignInOut,
    RefreshTokenIn,
    RefreshTokenOut,
    UserOut,
    UpdateUserIn,
)
from application.users.use_cases import (
    UserSignUpUseCase,
    UserSignInUseCase,
    RefreshAccessTokenUseCase,
    PasswordChangeUseCase,
    UpdateCurrentUserUseCase,
)

router = APIRouter(tags=["Accounts"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=SignUpOut)
async def sign_up(payload: SignUpIn):
    use_case = UserSignUpUseCase()
    return await use_case(payload.model_dump())


@router.post("/signin", response_model=SignInOut)
async def sign_in(email: EmailStr = Form(), password: str = Form()):
    use_case = UserSignInUseCase()
    return await use_case(email, password)


@router.post("/authentication/token-refresh", response_model=RefreshTokenOut)
async def token_refresh(refresh_token: RefreshTokenIn):
    use_case = RefreshAccessTokenUseCase()
    return await use_case(refresh_token)


@router.post("/authentication/password/change/")
async def change_user_password(
    old_password: str = Form(),
    new_password: str = Form(),
    user: User = Depends(get_current_user),
):
    use_case = PasswordChangeUseCase(user)
    await use_case(old_password, new_password)
    return {"detail": "New password has been saved."}


@router.get("/me/", response_model=UserOut)
async def retrieve_current_user(user: User = Depends(get_current_user)):
    return user


@router.patch("/me/", response_model=UserOut)
async def update_current_user(
    payload: UpdateUserIn, user: User = Depends(get_current_user)
):
    use_case = UpdateCurrentUserUseCase(user)
    return await use_case(payload.model_dump(exclude_unset=True))
