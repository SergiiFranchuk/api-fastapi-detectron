from celery import Celery

from application.constants import (
    FRAME_GENERATORS,
    ImageAnalysisOperationType,
    ImageAnalysisMLTool,
)
from application.analysis_processor import FrameAnalysisProcessor

celery = Celery("frame_analysis")

celery.config_from_object("application.settings", namespace="CELERY")
celery.autodiscover_tasks()


@celery.task()
def analyse_input_frames_task(
    source_path: str,
    frame_generator_name: str,
    ml_tool: str = ImageAnalysisMLTool.DETECTRON_2,
    analysis_task_type: str = ImageAnalysisOperationType.OBJECT_DETECTION,
) -> list:
    frame_collection = FRAME_GENERATORS[frame_generator_name](source_path)
    frame_processor = FrameAnalysisProcessor(
        ml_tool=ml_tool, analysis_task_type=analysis_task_type
    )

    return frame_processor.analyze_frames(frame_collection)
