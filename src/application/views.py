from fastapi import APIRouter, UploadFile, File, Depends

from application.users.dependencies import get_current_user
from application.use_cases import (
    DetectObjectsInVideoFileUseCase,
    CheckDetectionResultUseCase,
)
from application.users.models import User

router = APIRouter(prefix="/tasks", tags=["Detection tasks"])


@router.post("/video-objects-detection/")
async def detect_objects_in_video(
    video_file: UploadFile = File(...), user: User = Depends(get_current_user)
):
    use_case = DetectObjectsInVideoFileUseCase(user)
    return await use_case(video_file)


@router.get("/video-analysis-result/{task_id}/")
async def get_video_analysis_result(
    task_id: str, user: User = Depends(get_current_user)
):
    use_case = CheckDetectionResultUseCase(user)
    return await use_case(task_id)
