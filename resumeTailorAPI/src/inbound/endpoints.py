from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends, Body
from typing import Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.resumeTailorService.tailor_service import TailorService
from src.inbound.resume_processor import ResumeProcessor
from src.database import get_db
from src.models import User


class CreateUserRequest(BaseModel):
    firstName: str
    lastName: str


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
    # Get resume text from either text input or file
    resume_text = await ResumeProcessor.get_resume_text(resume_text, resume_file)
    
    # Call the service to tailor the resume
    tailored_response = await TailorService.tailor_resume_to_job(
        user_id, 
        resume_text, 
        job_description
    )
    
    return {
        "user_id": user_id,
        "resume_text": resume_text,
        "job_description": job_description,
        "tailored_response": tailored_response,
        "message": "Resume tailored successfully"
    }


@router.post("/api/v1/users")
def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    """
    Create a new user - Test endpoint for database
    
    Request body:
    {
        "firstName": "John",
        "lastName": "Doe"
    }
    """
    new_user = User(firstName=request.firstName, lastName=request.lastName)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "userId": new_user.userId,
        "firstName": new_user.firstName,
        "lastName": new_user.lastName,
        "message": "User created successfully"
    }



