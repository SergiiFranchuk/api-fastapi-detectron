import numpy as np
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor

from application import settings
from application.constants import ImageAnalysisMLTool, DETECTRON_MODEL_CONFIG_FILE_PATH
from application.interfaces import AbstractImageAnalysisMLModel


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


class ImageAnalysisMLModelFactory:
    def __init__(self):
        self.model_mapping = {
            ImageAnalysisMLTool.DETECTRON_2: self._create_detectron2_model,
            # could be added other models
        }

    def build_model(
        self,
        ml_model,
        process_type,
        threshold=settings.ML_MODEL_ANALYSIS_THRESHOLD,
        processing_device=settings.ML_MODEL_PROCESSING_DEVICE,
    ):
        if ml_model in self.model_mapping:
            model_creation_method = self.model_mapping[ml_model]
            return model_creation_method(process_type, threshold, processing_device)
        else:
            raise ValueError(f"Unsupported process_type: {process_type}")

    def _create_detectron2_model(self, analysis_type, threshold, processing_device):
        config = get_cfg()

        # Load model config and pretrained model
        config.merge_from_file(
            model_zoo.get_config_file(DETECTRON_MODEL_CONFIG_FILE_PATH[analysis_type])
        )
        config.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(
            DETECTRON_MODEL_CONFIG_FILE_PATH[analysis_type]
        )

        config.MODEL.ROI_HEADS.SCORE_THRESH_TEST = threshold
        config.MODEL.DEVICE = processing_device

        predictor = DefaultPredictor(config)
        metadata = MetadataCatalog.get(config.DATASETS.TRAIN[0])

        return Detectron2MLModel(predictor, metadata)
