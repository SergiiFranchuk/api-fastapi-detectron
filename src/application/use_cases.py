from celery.result import AsyncResult
from fastapi import UploadFile

from application.users.models import User
from application.utils import save_video_file
from application.tasks import detect_objects_on_video


class BaseUseCase:
    def __init__(self, user: User = None):
        self.user = user

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError


class StartDetectionUseCase(BaseUseCase):
    async def __call__(self, videofile: UploadFile):
        filepath = await save_video_file(videofile)
        task = detect_objects_on_video.delay(filepath)
        return {"task_id": task.id}


class CheckDetectionResultUseCase(BaseUseCase):
    async def __call__(self, task_id: str):
        task_result = AsyncResult(task_id)
        if task_result.ready():
            result = task_result.get()
            return {"task_id": task_id, "status": "Completed", "result": result}
        else:
            return {"task_id": task_id, "status": "In progress"}