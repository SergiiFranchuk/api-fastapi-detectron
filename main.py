from fastapi import FastAPI, UploadFile, File

from use_cases import StartDetectionUseCase, CheckDetectionResultUseCase

application = FastAPI()


@application.post("/video-analyze/")
async def detect_objects_on_video(videofile: UploadFile = File(...)):
    use_case = StartDetectionUseCase()
    return await use_case(videofile)


@application.post("/video-analyze-result/{task_id}/")
async def check_video_analyze_result(task_id: str):
    use_case = CheckDetectionResultUseCase()
    return await use_case(task_id)
