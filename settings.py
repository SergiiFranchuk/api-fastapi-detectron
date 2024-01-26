import os

DETECTION_THREASHOLD = 0.75

BASE_STORAGE_PATH = "storage/videos/"

CELERY_BROKER_URL = os.getenv("CELERY_BROKER", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BACKEND", default="redis://localhost:6379/0")

DETECTION_MODEL_CONFIG_FILE_PATH = "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"
