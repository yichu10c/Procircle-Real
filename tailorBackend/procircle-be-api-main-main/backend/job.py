"""
Instantiate App
"""
# Load ENV
import dotenv
dotenv.load_dotenv()

# Set service name for logging
import os
os.environ["SERVICE_NAME"] = "job_worker"

# Import celery and registered tasks
from job_worker.task import analyze_task
from job_worker.core import app
