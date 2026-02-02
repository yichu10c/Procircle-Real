from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends, Body
from typing import Optional
from sqlalchemy.orm import Session
from docx import Document
from pydantic import BaseModel
from src.resumeTailorService.tailor_service import TailorService
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


@router.get("/api/v1/users")
def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users - Test endpoint for database
    """
    users = db.query(User).all()
    return {
        "count": len(users),
        "users": [
            {"userId": u.userId, "firstName": u.firstName, "lastName": u.lastName}
            for u in users
        ]
    }


@router.get("/api/v1/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID
    """
    user = db.query(User).filter(User.userId == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "userId": user.userId,
        "firstName": user.firstName,
        "lastName": user.lastName
    }
