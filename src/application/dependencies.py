from fastapi import UploadFile, File, HTTPException

from application import settings
from application.constants import FileContentType
from application.exceptions import ValidationError
from application.validators import validate_file_content_type, validate_file_size


def validate_video_upload(video_file: UploadFile = File(...)) -> UploadFile:

    # Check if the uploaded file is a video based on its content type
    try:
        validate_file_content_type(video_file, FileContentType.VIDEO)
    except ValidationError:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a video file."
        )

    # Check if the file size exceeds limit
    try:
        validate_file_size(video_file, settings.UPLOAD_VIDEO_MAX_SIZE_MB * 1024 * 1024)
    except ValidationError:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Size should not exceed {settings.UPLOAD_VIDEO_MAX_SIZE_MB} MB.",
        )

    return video_file
