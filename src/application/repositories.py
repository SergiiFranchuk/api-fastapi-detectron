from application.common.repositories import TortoiseRepository
from application.models import Task


class TaskRepository(TortoiseRepository):
    model_class = Task

    async def get_by_worker_task_id(self, reference):
        return await self.model_class.get_or_none(worker_task_id=reference)

    async def update_by_worker_task_id(self, reference, data):
        return await self.model_class.filter(worker_task_id=reference).update(**data)
