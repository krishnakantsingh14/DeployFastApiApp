import os
from celery import Celery

# Get the broker URL and backend URL from environment variables
broker_url = os.getenv("CELERY_BROKER_URL", "amqp://guest@localhost//")
backend_url = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=broker_url,
    backend=backend_url
)

celery_app.conf.update(
    task_routes={
        "app.tasks.simulation": {"queue": "default"},
    },
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

import app.tasks
