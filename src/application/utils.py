import os
import pathlib
from typing import Generator
from uuid import uuid4
import numpy as np

import aiofiles
import cv2
from fastapi import UploadFile

from application import settings


async def save_video_file(video_file: UploadFile) -> str:
    filename = str(uuid4())
    extension = pathlib.Path(video_file.filename).suffix
    filepath = os.path.join(settings.BASE_STORAGE_PATH, f"{filename}{extension}")

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    async with aiofiles.open(filepath, "wb") as output_file:
        content = await video_file.read()
        await output_file.write(content)

    return filepath


def generate_frames_from_video(video_path: str) -> Generator[np.ndarray, None, None]:
    video_manager = cv2.VideoCapture(video_path)
    exist, frame = video_manager.read()
    while exist:
        yield frame
        exist, frame = video_manager.read()
    video_manager.release()
