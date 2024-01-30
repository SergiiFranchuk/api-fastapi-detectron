import os
from datetime import timedelta

DETECTION_THREASHOLD = 0.75

BASE_STORAGE_PATH = "storage/videos/"

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", default="secretkey")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
JWT_REFRESH_TOKEN_LIFETIME = timedelta(days=30)

CELERY_BROKER_URL = os.getenv("CELERY_BROKER", default="redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BACKEND", default="redis://localhost:6379/0")

DETECTION_MODEL_CONFIG_FILE_PATH = "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"

POSTGRES_DB = os.getenv("POSTGRES_DB", default="postgres")
POSTGRES_USER = os.getenv("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", default="postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", default=5432)


TORTOISE_ORM_CONFIG = {
    "connections": {
        "default": (
            f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
            f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        ),
    },
    "apps": {
        "application.users": {
            "models": ["application.users.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
