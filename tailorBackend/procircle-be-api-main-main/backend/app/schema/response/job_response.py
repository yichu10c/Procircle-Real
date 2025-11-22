"""
Job Response
"""
from typing import List, Optional

from app.schema.data.job import (
    JobShortDetailsItem,
    JobFullDetails,
    JobMatchResult,
    JobMatchAnalysisResult,
    AnalyzeResumeWithJobDescResult,
    JobMatchAnalysisWPAResult
)
from app.schema.response import BaseResponseSchema


class GetJobListResponse(BaseResponseSchema):
    data: List[JobShortDetailsItem] = []

class GetJobDetailsResponse(BaseResponseSchema):
    data: Optional[JobFullDetails] = None

class JobMatchResponse(BaseResponseSchema):
    data: JobMatchResult

class GetJobMatchHistoryResponse(BaseResponseSchema):
    data: List[JobMatchResult]

class AnalyzeJobMatchResponse(BaseResponseSchema):
    data: bool

class JobMatchAnalysisResponse(BaseResponseSchema):
    data: Optional[JobMatchAnalysisResult] = None

class AnalyzeResumeWithJobDescResponse(BaseResponseSchema):
    data: Optional[AnalyzeResumeWithJobDescResult] = None

class GetJobMatchAnalysisWPAResponse(BaseResponseSchema):
    data: Optional[JobMatchAnalysisWPAResult] = None
