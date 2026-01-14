from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pydantic import BaseModel
import uuid
from docx import Document

router = APIRouter()

class ResumeSubmission(BaseModel):
    user_id: str
    resume_text: str

class JobDescriptionSubmission(BaseModel):
    user_id: str
    job_description: str

@router.post("/api/v1/resume")
async def submit_resume(resume: ResumeSubmission):
    return {
        "resume_id": str(uuid.uuid4()),
        "user_id": resume.user_id,
        "message": "Resume submitted successfully"
    }

@router.post("/api/v1/job-description")
async def submit_job_description(job: JobDescriptionSubmission):
    return {
        "job_id": str(uuid.uuid4()),
        "user_id": job.user_id,
        "message": "Job description submitted successfully"
    }

@router.post("/api/v1/resume/upload")
async def upload_resume_docx(user_id: str = Form(...), file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported.")
    try:
        contents = await file.read()
        with open("temp_resume.docx", "wb") as f:
            f.write(contents)
        doc = Document("temp_resume.docx")
        text = "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
    return {
        "resume_id": str(uuid.uuid4()),
        "user_id": user_id,
        "extracted_text": text,
        "message": "Resume .docx uploaded and processed successfully"
    }
