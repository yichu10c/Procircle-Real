"""
Job Request Spec
"""
from typing import Optional
from pydantic import BaseModel


class JobMatchSpec(BaseModel):
    resume_id: int
    job_id: Optional[int] = None
    job_desc_id: Optional[int] = None
    job_title: Optional[str] = None
    job_desc_text: Optional[str] = None


class AnalyzeJobMatchSpec(BaseModel):
    job_match_id: int


class AnalyzeResumeWithJobDescSpec(BaseModel):
    resume_id: int
    job_title: str
    job_desc: str
