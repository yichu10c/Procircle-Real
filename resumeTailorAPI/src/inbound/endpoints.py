from fastapi import APIRouter, UploadFile, File, Form, Depends
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
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Tailor a resume to a job description.
    
    Multipart form data:
    - user_id: required
    - job_description: required
    - resume_file: required (.docx file)
    """
    saved_resume = await ResumeProcessor.save_resume_to_db(
        user_id=int(user_id),
        resume_file=resume_file,
        db=db
    )

    tailored_response = await TailorService.tailor_resume_to_job(
        resume_id=saved_resume.resumeId,
        job_description=job_description,
        db=db
    )
    
    return {
        "user_id": user_id,
        "resume_id": saved_resume.resumeId,
        "resume_text": saved_resume.resumeText,
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
