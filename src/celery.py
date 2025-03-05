from celery import Celery

from .settings import get_settings

celery_app = Celery(
    "users",
    broker=get_settings().redis_url,
)
