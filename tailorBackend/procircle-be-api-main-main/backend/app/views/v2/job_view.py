"""
Job View
"""
from fastapi import APIRouter, Depends, File, Form, Request, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.v2 import job_controller
from app.tools.sql import connection
from app.tools.security import auth
from app.schema.data.job import AnalyzeResumeWithJobDescResult, JobMatchAnalysisWPAResult
from app.schema.request.job_request import AnalyzeResumeWithJobDescSpec
from app.schema.response import ResponseStatusEnum
from app.schema.response.job_response import AnalyzeResumeWithJobDescResponse, GetJobMatchAnalysisWPAResponse

router = APIRouter(prefix="/jobs", dependencies=[Depends(auth.api_authentication)])


@router.post("/analyze")
async def analyze_resume_with_job_desc(
    request: Request,
    spec: AnalyzeResumeWithJobDescSpec,
    session: AsyncSession = Depends(connection.get_session),
) -> AnalyzeResumeWithJobDescResponse:
    job_match_id = await job_controller.handle_analyze_resume_with_job_desc(request, session, spec)
    return AnalyzeResumeWithJobDescResponse(
        data=AnalyzeResumeWithJobDescResult(
            job_match_id=job_match_id
        ),
        status=ResponseStatusEnum.SUCCESS
    )


@router.get("/analyze/result")
async def get_analysis_result(
    request: Request,
    job_match_id: int,
    session: AsyncSession = Depends(connection.get_session)
) -> GetJobMatchAnalysisWPAResponse:
    result = await job_controller.handle_get_job_analysis_wpa_result(
        session=session,
        request=request,
        job_match_id=job_match_id
    )
    return GetJobMatchAnalysisWPAResponse(data=result)
