from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from docx import Document
from resumeTailorService.tailor_service import TailorService

router = APIRouter()

@router.post("/api/v1/tailor-resume")
async def tailor_resume(
    user_id: str = Form(...),
    job_description: str = Form(...),
    resume_text: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None)
):
    """
    Tailor a resume to a job description.
    Accepts either resume_text OR resume_file (not both).
    
    Multipart form data:
    - user_id: required
    - job_description: required
    - resume_text: optional (text input)
    - resume_file: optional (.docx file)
    """
    
    # Validate that either resume_text or resume_file is provided
    if not resume_text and not resume_file:
        raise HTTPException(
            status_code=400,
            detail="Provide either resume_text or resume_file"
        )
    
    if resume_text and resume_file:
        raise HTTPException(
            status_code=400,
            detail="Provide either resume_text OR resume_file, not both"
        )
    
    # Extract resume text from file if provided
    if resume_file:
        if not resume_file.filename.endswith(".docx"):
            raise HTTPException(status_code=400, detail="Only .docx files are supported.")
        try:
            contents = await resume_file.read()
            with open("temp_resume.docx", "wb") as f:
                f.write(contents)
            doc = Document("temp_resume.docx")
            resume_text = "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process file: {e}")
    
    # Call the orchestrator service to tailor the resume
    tailored_response = await TailorService.tailor_resume_to_job(user_id, resume_text, job_description)
    
    return {
        "user_id": user_id,
        "resume_text": resume_text,
        "job_description": job_description,
        "tailored_response": tailored_response,
        "message": "Resume tailored successfully"
    }
