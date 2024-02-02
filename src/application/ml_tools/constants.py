from enum import Enum


class ImageAnalysisMLTool(str, Enum):
    DETECTRON_2 = "detectron_2"


class ImageAnalysisOperationType(str, Enum):
    OBJECT_DETECTION = "object_detection"


class Detectron2TypeModel(str, Enum):
    DETECTION = "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"


DETECTRON_MODEL_CONFIG_FILE_PATH_MAP = {
    ImageAnalysisOperationType.OBJECT_DETECTION: Detectron2TypeModel.DETECTION
}
