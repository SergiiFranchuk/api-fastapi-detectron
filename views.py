from fastapi import APIRouter, UploadFile, File, Depends

from depndencies import get_current_user_id
from use_cases import StartDetectionUseCase, CheckDetectionResultUseCase

router = APIRouter(prefix="/tasks", tags=["Detection tasks"])


@router.post("/video-analyze/")
async def detect_objects_on_video(
    videofile: UploadFile = File(...), user_id: int = Depends(get_current_user_id)
):
    use_case = StartDetectionUseCase(user_id)
    return await use_case(videofile)


@router.post("/video-analyze-result/{task_id}/")
async def check_video_analyze_result(
    task_id: str, user_id: int = Depends(get_current_user_id)
):
    use_case = CheckDetectionResultUseCase(user_id)
    return await use_case(task_id)
