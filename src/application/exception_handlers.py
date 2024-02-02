from fastapi import Request
from fastapi.responses import JSONResponse

from application.exceptions import CannotOpenVideoFileError, CannotReadVideoFileError


async def open_video_file_exception_handler(
    request: Request, exception: CannotOpenVideoFileError
) -> JSONResponse:
    return JSONResponse(
        status_code=400, content={"detail": "The video file could not be opened"}
    )


async def read_video_file_exception_handler(
    request: Request, exc: CannotReadVideoFileError
) -> JSONResponse:
    return JSONResponse(
        status_code=400, content={"detail": "Video file is corrupted or unreadable"}
    )
