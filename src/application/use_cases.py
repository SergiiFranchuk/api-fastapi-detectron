from celery.result import AsyncResult
from fastapi import UploadFile

from application.users.models import User
from application.utils import save_video_file
from application.tasks import analyse_input_frames_task
from application.validators import verify_video_file_integrity


class BaseUseCase:
    def __init__(self, user: User = None):
        self.user = user

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError


class DetectObjectsInVideoFileUseCase(BaseUseCase):
    async def __call__(self, video_file: UploadFile) -> dict:
        filepath = await save_video_file(video_file)
        verify_video_file_integrity(filepath)
        task = analyse_input_frames_task.delay(filepath)
        return {"task_id": task.id}


class GetVideoAnalysisResultUseCase(BaseUseCase):
    async def __call__(self, task_id: str) -> dict:
        task_result = AsyncResult(task_id)

        result_data = {
            "success": task_result.successful(),
            "ready": task_result.ready(),
            "result": None,
            "error": None,
        }

        if task_result.successful():
            result_data["result"] = task_result.result
        elif task_result.failed():
            result_data["error"] = task_result.result.args

        return result_data
