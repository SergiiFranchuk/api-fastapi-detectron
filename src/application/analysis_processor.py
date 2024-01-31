from typing import Generator

from application.ml_models import ImageAnalysisMLModelFactory


class FrameAnalysisProcessor:
    def __init__(self, ml_tool, analysis_task_type):
        self.ml_model = ImageAnalysisMLModelFactory().build_model(
            ml_tool, analysis_task_type
        )

    def analyze_frames(self, frame_collection: Generator) -> list:
        result = []
        for frame in frame_collection:
            result.append(self.ml_model.analyze_frame(frame))
        return result
