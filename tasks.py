from celery import Celery

from detector import Detector

celery = Celery("detectron")

celery.config_from_object("settings", namespace="CELERY")
celery.autodiscover_tasks()


@celery.task()
def detect_objects_on_video(filepath: str) -> list:
    detector = Detector()
    return detector.detect_from_video(filepath)
