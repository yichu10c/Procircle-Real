from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI()


class ResumeSubmission(BaseModel):
    user_id: str
    resume_text: str


class JobDescriptionSubmission(BaseModel):
    user_id: str
    job_description: str


@app.post("/api/v1/resume")
async def submit_resume(resume: ResumeSubmission):
    return {
        "resume_id": str(uuid.uuid4()),
        "user_id": resume.user_id,
        "message": "Resume submitted successfully"
    }


@app.post("/api/v1/job-description")
async def submit_job_description(job: JobDescriptionSubmission):
    return {
        "job_id": str(uuid.uuid4()),
        "user_id": job.user_id,
        "message": "Job description submitted successfully"
    }
