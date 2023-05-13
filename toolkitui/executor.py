from celery import Celery
import os

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

app = Celery('tasks', broker=broker_url, backend=result_backend)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Los_Angeles',
    enable_utc=True,
)
