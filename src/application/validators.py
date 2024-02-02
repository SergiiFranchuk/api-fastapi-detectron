import cv2
from fastapi import UploadFile

from application.constants import FileContentType
from application.exceptions import (
    ValidationError,
    CannotOpenVideoFileError,
    CannotReadVideoFileError,
)


def validate_file_content_type(file: UploadFile, file_type: FileContentType) -> None:
    if not file.content_type.startswith(file_type):
        raise ValidationError()


def validate_file_size(file, limit) -> None:
    if file.size > limit:
        raise ValidationError()


def verify_video_file_integrity(video_path: str) -> bool:
    capture = cv2.VideoCapture(video_path)
    if not capture.isOpened():
        raise CannotOpenVideoFileError()
    success, frame = capture.read()
    capture.release()
    if not success:
        raise CannotReadVideoFileError()
    return True
