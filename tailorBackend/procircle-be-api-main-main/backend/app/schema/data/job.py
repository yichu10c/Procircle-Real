"""
Job Data
"""
import datetime as dt
from pydantic import BaseModel, field_validator
from typing import Optional

from app.schema.data.asset import AssetStorageType


class JobAnalysisStatus:
    SUCCESS = 1
    FAILED_RETRYABLE = 0
    FAILED_NON_RETRYABLE = -1


class JobShortDetailsItem(BaseModel):
    id: int
    updated_at: dt.datetime
    job_title: str
    company_name: str
    industries: str
    location: str
    seniority_level: str


class JobFullDetails(BaseModel):
    id: int
    created_at: dt.datetime
    updated_at: Optional[dt.datetime]
    job_title: str
    company_name: str
    company_link: str
    job_description: str
    seniority_level: str
    employment_type: str
    job_function: str
    industries: str
    location: str
    logo: str


class JobMatchResult(BaseModel):
    job_match_id: int
    resume_id: int
    score: float
    job_id: Optional[int] = None
    job_desc_id: Optional[int] = None
    job_title: Optional[str] = None
    job_desc_text: Optional[str] = None
    created_at: dt.datetime


class JobMatchAnalysisResult(BaseModel):
    analysis_id: int
    created_at: dt.datetime
    status_code: int
    score: float
    asset_type: AssetStorageType | str
    asset_url: str

    @field_validator("asset_type")
    def validate_asset_type(cls, value: AssetStorageType | str):
        if isinstance(value, AssetStorageType):
            return value
        return getattr(AssetStorageType, value)


class JobMatchAnalysisWPAResult(BaseModel):
    analysis_id: int
    created_at: dt.datetime
    status_code: int
    score: float | None
    verdict: str
    verdict_description: str
    asset_type: AssetStorageType | str
    asset_url: str

    @field_validator("asset_type")
    def validate_asset_type(cls, value: AssetStorageType | str):
        if isinstance(value, AssetStorageType):
            return value
        return getattr(AssetStorageType, value)


class AnalyzeResumeWithJobDescResult(BaseModel):
    job_match_id: int
