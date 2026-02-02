from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models import User


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
