"""
Job Controller V2
"""
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import job_query
from app.schema.request.job_request import AnalyzeResumeWithJobDescSpec
from app.tools.security import auth
from job_worker.task import analyze_task

from typing import Optional
from app.repository import analysis_query, asset_query, job_query
from app.schema.data.asset import AssetStorageType
from app.schema.data.job import JobMatchAnalysisWPAResult
from app.schema.models.job_model import Job
from app.utils.exceptions import ApplicationException
from app.tools.analysis import matcher
from app.tools.cache import lru
from app.tools.resource import file
from app.tools.security import auth
from job_worker.task import analyze_task
from tools.observability.log import get_logger
from tools.verdict import get_wpa_verdict


async def handle_analyze_resume_with_job_desc(
    request: Request,
    session: AsyncSession,
    spec: AnalyzeResumeWithJobDescSpec
) -> int:
    logger = await get_logger(request)
    try:
        # get current user
        logger.info("Get user...")
        user = auth.get_current_user(request)

        # check existing job match, user + resume id + job desc
        logger.info("Get job match...")
        job_match = await job_query.get_job_match_by_user_resume_jobdesc(
            session=session,
            user_id=user.id,
            resume_id=spec.resume_id,
            job_desc=spec.job_desc,
        )
        logger.info(f"job match = {job_match}")

        # if exist, check status code
        if job_match:
            job_match_id = job_match["id"]
            analysis = await analysis_query.get_analysis(session, user.id, job_match_id)

            # if the job match exists but the analysis does not, continue.
            # This indicates the job is still running or the job worker is dead
            if analysis:
                # check current analysis completion status
                match analysis["status_code"]:
                    # analysis is completed, return immediately
                    case 1: return job_match_id
                    # analysis is failed, non retryable, return immediately
                    case -1: return job_match_id
                    # analysis is failed, but retryable, continue
                    case 0: pass

        # if not exist, create job match, save user + resume + job desc -> new job match id
        else:
            logger.info(f"insert job match")
            job_match_id = await job_query.insert_job_match(
                session=session,
                user_id=user.id,
                resume_id=spec.resume_id,
                job_title=spec.job_title,
                job_desc_text=spec.job_desc
            )

        # launch async task to job worker
        analyze_task.start_job_match_analysis_wpa.delay(job_match_id)
        logger.info(f"finished enqueue")
        return job_match_id
    except Exception as error:
        logger.error(f"Error during trigger analyze. {error=}")
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(error)


async def handle_get_job_analysis_wpa_result(
    session: AsyncSession,
    request: Request,
    job_match_id: int
) -> Optional[JobMatchAnalysisWPAResult]:
    """
    """
    try:
        user = auth.get_current_user(request)
        result = await analysis_query.get_analysis(session, user.id, job_match_id)
        if result:
            verdict_dto = get_wpa_verdict(result["score"])
            return JobMatchAnalysisWPAResult(
                analysis_id=result["id"],
                created_at=result["created_at"],
                status_code=result["status_code"],
                score=result["score"],
                verdict=verdict_dto.verdict,
                verdict_description=verdict_dto.desc,
                asset_type=result["asset_type"],
                asset_url=result["asset_url"],
            )
    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(error)
