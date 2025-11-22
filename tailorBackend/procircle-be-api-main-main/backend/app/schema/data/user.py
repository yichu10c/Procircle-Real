"""
User Data
"""
from pydantic import BaseModel


class UserToken(BaseModel):
    user_id: int
    expired_at: float
