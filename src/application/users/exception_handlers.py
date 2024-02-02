from fastapi import Request
from fastapi.responses import JSONResponse


from application.users.exceptions import MismatchPasswordError


async def password_mismatch_exception_handler(
    request: Request, exception: MismatchPasswordError
) -> JSONResponse:
    return JSONResponse(
        status_code=400, content={"detail": "The two password fields didn't match."}
    )
