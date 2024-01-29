from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    def __init__(self, detail: tuple = ("Could not validate credentials",)):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
