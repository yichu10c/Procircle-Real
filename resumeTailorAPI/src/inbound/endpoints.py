from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
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
    resume_id: int = Form(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Tailor a resume to a job description.
    
    Multipart form data:
    - resume_id: required (ID of previously uploaded resume)
    - job_description: required
    """
    try:
        tailored_response = await TailorService.tailor_resume_to_job(
            resume_id=resume_id,
            job_description=job_description,
            db=db
        )
        
        return {
            "resume_id": resume_id,
            "job_description": job_description,
            "tailored_response": tailored_response,
            "message": "Resume tailored successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


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
    try:
        new_user = User(firstName=request.firstName, lastName=request.lastName)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "userId": new_user.userId,
            "firstName": new_user.firstName,
            "lastName": new_user.lastName,
            "createdAt": new_user.createdAt.isoformat() if new_user.createdAt else None,
            "message": "User created successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")


@router.post("/api/v1/users/{user_id}/resumes")
async def upload_resume(
    user_id: int,
    resume_file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a resume for a specific user without tailoring.
    
    Path parameter:
    - user_id: The user ID
    
    Multipart form data:
    - resume_file: required (.docx file)
    """
    try:
        user = db.query(User).filter(User.userId == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        saved_resume = await ResumeProcessor.save_resume_to_db(
            user_id=user_id,
            resume_file=resume_file,
            db=db
        )
        
        return {
            "resumeId": saved_resume.resumeId,
            "userId": saved_resume.userId,
            "fileName": saved_resume.fileName,
            "createdAt": saved_resume.createdAt.isoformat() if saved_resume.createdAt else None,
            "message": "Resume uploaded successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload resume: {str(e)}")
