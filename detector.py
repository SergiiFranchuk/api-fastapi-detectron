from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2 import model_zoo
import cv2
import numpy as np

import settings


class Detector:
    def __init__(self):
        self.cfg = get_cfg()

        # Load model config and pretrained model
        self.cfg.merge_from_file(model_zoo.get_config_file(settings.DETECTION_MODEL_CONFIG_FILE_PATH))
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(settings.DETECTION_MODEL_CONFIG_FILE_PATH)

        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = settings.DETECTION_THREASHOLD
        self.cfg.MODEL.DEVICE = "cpu"  # Use CPU for inference

        self.predictor = DefaultPredictor(self.cfg)
        self.metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])

    def detect_from_image(self, image: np.ndarray | str):

        if isinstance(image, str):
            image = cv2.imread(image)

        predictions = self.predictor(image)

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

    def detect_from_video(self, video_path: str) -> list:
        # open the video
        video_manager = cv2.VideoCapture(video_path)

        video_objects_data = []
        exist, frame = video_manager.read()
        frame_num = 0
        while exist:
            frame_num += 1
            frame_data = self.detect_from_image(frame)
            video_objects_data.append(frame_data)

            exist, frame = video_manager.read()

        return video_objects_data
