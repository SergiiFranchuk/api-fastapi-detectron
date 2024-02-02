import datetime

from celery import Celery, current_task

from application.ml_tools.constants import (
    ImageAnalysisMLTool,
    ImageAnalysisOperationType,
)
from application.ml_tools.factories import ml_model_factory_map
from application.ml_tools.services import FrameAnalysisProcessor
from application.repositories import TaskRepository
from application.utils import generate_frames_from_video, async_to_sync

celery = Celery("frame_analysis")

celery.config_from_object("application.settings", namespace="CELERY")
celery.autodiscover_tasks()


@celery.task()
def analyse_input_frames_task(
    source_path: str,
    ml_tool_name: str = ImageAnalysisMLTool.DETECTRON_2,
    analysis_task_type: str = ImageAnalysisOperationType.OBJECT_DETECTION,
) -> list:
    task_id = current_task.request.id

    frame_collection = generate_frames_from_video(source_path)

    ml_model = ml_model_factory_map[ml_tool_name]().build_model(analysis_task_type)
    frame_processor = FrameAnalysisProcessor(ml_model)

    result = frame_processor.analyze_frames(frame_collection)

    # updating task representation model with finished time
    async_to_sync(
        TaskRepository().update_by_worker_task_id,
        task_id,
        {"finished_at": datetime.datetime.now()},
    )

    return result
