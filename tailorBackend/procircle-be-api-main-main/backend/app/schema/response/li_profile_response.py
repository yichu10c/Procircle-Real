"""
LinkedIn Profile Response Schema
"""
from typing import Optional
from app.schema.response import BaseResponseSchema
from app.schema.data.li_profile import LinkedInProfileResult, AnalyzeLinkedInProfileResult


class AnalyzeLinkedInProfileResponse(BaseResponseSchema):
    data: Optional[AnalyzeLinkedInProfileResult] = None


class GetLinkedInProfileAnalysisResponse(BaseResponseSchema):
    data: Optional[LinkedInProfileResult] = None
