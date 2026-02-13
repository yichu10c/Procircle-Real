from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import User, Resume


router = APIRouter()


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


@router.get("/api/v1/resumes/{resume_id}")
def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """
    Get a specific resume by ID
    """
    resume = db.query(Resume).filter(Resume.resumeId == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {
        "resumeId": resume.resumeId,
        "userId": resume.userId,
        "fileName": resume.fileName,
        "resumeText": resume.resumeText
    }


@router.get("/api/v1/resumes")
def get_all_resumes(db: Session = Depends(get_db)):
    """
    Get all resumes from the database
    """
    resumes = db.query(Resume).all()
    return {
        "count": len(resumes),
        "resumes": [
            {
                "resumeId": r.resumeId,
                "userId": r.userId,
                "fileName": r.fileName,
                "resumeText": r.resumeText
            }
            for r in resumes
        ]
    }


@router.get("/api/v1/users/{user_id}/resumes")
def get_user_resumes(user_id: int, db: Session = Depends(get_db)):
    """
    Get all resumes for a specific user
    """
    user = db.query(User).filter(User.userId == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    resumes = db.query(Resume).filter(Resume.userId == user_id).all()
    return {
        "userId": user_id,
        "userName": f"{user.firstName} {user.lastName}",
        "count": len(resumes),
        "resumes": [
            {
                "resumeId": r.resumeId,
                "fileName": r.fileName,
                "resumeText": r.resumeText
            }
            for r in resumes
        ]
    }
