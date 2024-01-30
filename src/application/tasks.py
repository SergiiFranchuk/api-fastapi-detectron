from celery import Celery

from application.detector import Detector

celery = Celery("detectron")

celery.config_from_object("application.settings", namespace="CELERY")
celery.autodiscover_tasks()


@celery.task()
def detect_objects_on_video(filepath: str) -> list:
    detector = Detector()
    return detector.detect_from_video(filepath)
