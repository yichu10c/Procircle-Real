"""
Job View
"""
from fastapi import APIRouter, Depends, File, Form, Request, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.v1 import job_controller
from app.tools.sql import connection
from app.tools.security import auth
from app.schema.request.job_request import AnalyzeJobMatchSpec, JobMatchSpec
from app.schema.response.job_response import (
    AnalyzeJobMatchResponse, GetJobDetailsResponse, GetJobListResponse,
    GetJobMatchHistoryResponse, JobMatchResponse, JobMatchAnalysisResponse
)


router = APIRouter(prefix="/jobs")


@router.get("")
async def get_job_list(
    page: int = Query(1),
    row: int = Query(10),
    session: AsyncSession = Depends(connection.get_session),
) -> GetJobListResponse:
    """
    Get a list of job
    """
    result = await job_controller.get_job_list(session, page, row)
    return GetJobListResponse(data=result)


@router.get("/{job_id}")
async def get_job_details(
    job_id: int,
    session: AsyncSession = Depends(connection.get_session),
) -> GetJobDetailsResponse:
    """
    Get Job Details
    """
    result = await job_controller.get_job_details(session, job_id)
    return GetJobDetailsResponse(data=result)


@router.post("/match", dependencies=[Depends(auth.api_authentication)])
async def score_job_match(
    request: Request,
    spec: JobMatchSpec,
    session: AsyncSession = Depends(connection.get_session),
) -> JobMatchResponse:
    """
    Calulcate job matching score using existing resume asset between:
    - job desc file id
    - job desc string
    - job id
    """
    result = await job_controller.job_match(
        session=session,
        request=request,
        resume_id=spec.resume_id,
        job_id=spec.job_id,
        job_desc_id=spec.job_desc_id,
        job_title=spec.job_title,
        job_desc_text=spec.job_desc_text,
    )

    return JobMatchResponse(data=result)


@router.post("/match-file", dependencies=[Depends(auth.api_authentication)])
async def score_job_match_file(
    request: Request,
    resume_id: int = Form(...),
    job_desc_file: UploadFile = File(...),
    session: AsyncSession = Depends(connection.get_session),
) -> JobMatchResponse:
    """
    Calulcate job matching score using uploaded file
    """
    result = await job_controller.job_match_with_file(
        session=session,
        request=request,
        resume_id=resume_id,
        job_desc_file=job_desc_file
    )

    return JobMatchResponse(data=result)


@router.post("/match-files", dependencies=[Depends(auth.api_authentication)])
async def score_job_match_files(
    request: Request,
    resume_file: UploadFile = File(...),
    job_desc_file: UploadFile = File(...),
    session: AsyncSession = Depends(connection.get_session),
) -> JobMatchResponse:
    """
    Calulcate job matching score using uploaded file
    """
    result = await job_controller.job_match_with_files(
        session=session,
        request=request,
        resume_file=resume_file,
        job_desc_file=job_desc_file
    )

    return JobMatchResponse(data=result)


@router.get("/match/history", dependencies=[Depends(auth.api_authentication)])
async def get_job_match_history(
    request: Request,
    page: int = 1,
    row: int = 10,
    session: AsyncSession = Depends(connection.get_session),
) -> GetJobMatchHistoryResponse:
    """
    Get Job Matching History
    """
    result = await job_controller.get_job_match_history(session, request, page, row)

    return GetJobMatchHistoryResponse(data=result)


@router.post("/analyze", dependencies=[Depends(auth.api_authentication)])
async def analyze_job_match(
    request: Request,
    spec: AnalyzeJobMatchSpec,
    session: AsyncSession = Depends(connection.get_session),
) -> AnalyzeJobMatchResponse:
    """
    Analyze job matching result using OpenAI to evaluate user's resume
    """
    result = await job_controller.analyze_job_match(session, request, spec.job_match_id)
    return AnalyzeJobMatchResponse(data=result)


@router.get("/analyze/result", dependencies=[Depends(auth.api_authentication)])
async def get_analysis_result(
    request: Request,
    job_match_id: int,
    session: AsyncSession = Depends(connection.get_session),
) -> JobMatchAnalysisResponse:
    """
    Analyze job matching result using OpenAI to evaluate user's resume
    """
    result = await job_controller.get_job_analysis_result(session, request, job_match_id)
    return JobMatchAnalysisResponse(data=result)
