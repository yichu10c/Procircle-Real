"""
Job Worker Core File
"""
import os
import celery

app = celery.Celery(
    "procircle-job-worker",
    broker=os.environ["RABBITMQ_HOST"],
)
