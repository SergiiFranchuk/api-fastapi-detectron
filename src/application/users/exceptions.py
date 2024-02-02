from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class MismatchPasswordError(Exception):
    """Error if different passwords while sign up"""


class PermissionDeniedError(Exception):
    """User does not meet the existing requirements for a specific action."""
