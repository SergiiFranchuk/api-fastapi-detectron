import numpy as np

from application.ml_tools.interfaces import AbstractImageAnalysisMLModel


class Detectron2MLModel(AbstractImageAnalysisMLModel):
    def __init__(self, predictor, metadata):
        self.predictor = predictor
        self.metadata = metadata

    def analyze_frame(self, frame: np.ndarray) -> dict:

        predictions = self.predictor(frame)

        # Get the detected instances
        instances = predictions["instances"]
        labels = instances.pred_classes.tolist()
        scores = instances.scores.tolist()

        # Create a dictionary to store object labels and scores for this frame
        frame_data = {}

        for label, score in zip(labels, scores):
            object_name = self.metadata.thing_classes[label]
            frame_data[object_name] = round(score, 2)

        return frame_data
