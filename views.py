from fastapi import APIRouter, UploadFile, File, Depends

from users.depndencies import get_current_user
from use_cases import StartDetectionUseCase, CheckDetectionResultUseCase
from users.models import User

router = APIRouter(prefix="/tasks", tags=["Detection tasks"])


@router.post("/video-analyze/")
async def detect_objects_on_video(
    videofile: UploadFile = File(...), user: User = Depends(get_current_user)
):
    use_case = StartDetectionUseCase(user)
    return await use_case(videofile)


@router.post("/video-analyze-result/{task_id}/")
async def check_video_analyze_result(
    task_id: str, user: User = Depends(get_current_user)
):
    use_case = CheckDetectionResultUseCase(user)
    return await use_case(task_id)
