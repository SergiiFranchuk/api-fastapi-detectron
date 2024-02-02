from fastapi import APIRouter, UploadFile, Depends

from application.dependencies import validate_video_upload
from application.schemas import TaskResultOut, TaskOut
from application.users.dependencies import get_current_user
from application.use_cases import (
    DetectObjectsInVideoFileUseCase,
    GetVideoAnalysisResultUseCase,
)
from application.users.models import User


router = APIRouter(prefix="/tasks", tags=["Detection tasks"])


@router.post("/video-objects-detection/", response_model=TaskOut)
async def detect_objects_in_video(
    video_file: UploadFile = Depends(validate_video_upload),
    user: User = Depends(get_current_user),
):
    use_case = DetectObjectsInVideoFileUseCase(user)
    return await use_case(video_file)


@router.get("/video-analysis-result/{task_id}/", response_model=TaskResultOut)
async def get_video_analysis_result(
    task_id: str, user: User = Depends(get_current_user)
):
    use_case = GetVideoAnalysisResultUseCase(user)
    return await use_case(task_id)
