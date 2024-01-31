from enum import Enum

from application.utils import generate_frames_from_video


class FrameGenerator(str, Enum):
    VIDEO_FILE = "video_file_frame_generator"


class ImageAnalysisMLTool(str, Enum):
    DETECTRON_2 = "detectron_2"


class ImageAnalysisOperationType(str, Enum):
    OBJECT_DETECTION = "object_detection"


DETECTRON_MODEL_CONFIG_FILE_PATH = {
    "object_detection": "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"
}


FRAME_GENERATORS = {
    FrameGenerator.VIDEO_FILE.value: generate_frames_from_video,
}
