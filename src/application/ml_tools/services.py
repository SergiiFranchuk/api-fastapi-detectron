from typing import Generator


class FrameAnalysisProcessor:
    def __init__(self, ml_model):
        self.ml_model = ml_model

    def analyze_frames(self, frame_collection: Generator) -> list:
        result = []
        for frame in frame_collection:
            result.append(self.ml_model.analyze_frame(frame))
        return result
