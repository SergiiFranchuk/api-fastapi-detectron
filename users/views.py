from fastapi import APIRouter

from users.schemas import SignUpIn, SignUpOut, SignIn, SignInOut
from users.use_cases import UserSignUpUseCase, UserSignInUseCase

router = APIRouter()


@router.post("/signup", response_model=SignUpOut)
async def sign_up(payload: SignUpIn):
    use_case = UserSignUpUseCase()
    return await use_case(payload.model_dump())


@router.post("/signin", response_model=SignInOut)
async def sign_in(credentials: SignIn):
    use_case = UserSignInUseCase()
    return await use_case(credentials.model_dump())
