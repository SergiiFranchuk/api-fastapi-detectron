import uuid

from celery.result import AsyncResult
from fastapi import UploadFile

from application.repositories import TaskRepository
from application.users.exceptions import PermissionDeniedError
from application.users.models import User
from application.utils import save_video_file
from application.tasks import analyse_input_frames_task
from application.validators import verify_video_file_integrity


class BaseUseCase:
    def __init__(self, user: User = None):
        self.user = user
        self.tasks = TaskRepository()

    async def __call__(self, *args, **kwargs):
        raise NotImplementedError


class DetectObjectsInVideoFileUseCase(BaseUseCase):
    async def __call__(self, video_file: UploadFile) -> dict:
        filepath = await save_video_file(video_file)
        verify_video_file_integrity(filepath)
        task = analyse_input_frames_task.delay(filepath)
        await self.tasks.create(
            {"id": uuid.uuid4(), "owner_id": self.user.id, "worker_task_id": task.id}
        )

        return {"task_id": task.id}


class GetVideoAnalysisResultUseCase(BaseUseCase):
    async def __call__(self, worker_task_id: str) -> dict:
        worker_task_result = AsyncResult(worker_task_id)

        task = await self.tasks.get_by_worker_task_id(worker_task_id)

        if not self.user.id == task.owner_id:
            raise PermissionDeniedError()

        result_data = {
            "success": worker_task_result.successful(),
            "ready": worker_task_result.ready(),
            "result": None,
            "error": None,
        }

        if worker_task_result.successful():
            result_data["result"] = worker_task_result.result
        elif worker_task_result.failed():
            result_data["error"] = worker_task_result.result.args

        return result_data
