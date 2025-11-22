"""LinkedIn Profile Request Spec"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr

class AnalyzeLinkedInProfileSpec(BaseModel):
    # Fields from the form
    email: EmailStr
    headline: Optional[str] = None
    current_position: Optional[str] = None
    about: Optional[str] = None
    education: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None
    licenses_certifications: Optional[str] = None

    job_types: str

    hcaptcha_token: str

    # Optional; any value is replaced by the verified WordPress user id
    wp_user_id: Optional[int] = None

    # Computed profile_data
    profile_data: Optional[Dict[str, Any]] = None
