import asyncio
import os
import pathlib
from typing import Generator, Callable
from uuid import uuid4
import numpy as np

import aiofiles
import cv2
from fastapi import UploadFile
from tortoise import Tortoise

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


async def connect_db():
    await Tortoise.init(config=settings.TORTOISE_ORM_CONFIG)


async def disconnect_db():
    await Tortoise.close_connections()


async def database_wrapper(func: Callable, *args, **kwargs):
    try:
        await connect_db()
        result = await func(*args, **kwargs)
    finally:
        await disconnect_db()

    return result


def async_to_sync(func: Callable, *args, **kwargs):
    return asyncio.run(database_wrapper(func, *args, **kwargs))
