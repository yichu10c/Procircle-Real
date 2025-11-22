import datetime as dt
from typing import Any, Dict, List, Optional, Union

from fastapi import Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import analysis_query, asset_query, job_query
from app.schema.data.asset import AssetStorageType
from app.schema.data.job import JobFullDetails, JobMatchResult, JobMatchAnalysisResult, JobAnalysisStatus
from app.schema.models.job_model import Job
from app.utils.exceptions import ApplicationException
from app.tools.analysis import matcher
from app.tools.cache import lru
from app.tools.resource import file
from app.tools.security import auth
from job_worker.task import analyze_task
from tools.aws import s3


@lru.cache(ttl=60)
async def get_job_list(
    session: AsyncSession,
    page: int,
    row: int
) -> Union[List[Job], str]:
    """
    """
    try:
        return await job_query.get_job_list(session, page, row)
    except Exception as error:
        raise ApplicationException(error)


@lru.cache(ttl=60)
async def get_job_details(
    session: AsyncSession,
    job_id: int,
) -> Optional[JobFullDetails]:
    """
    """
    try:
        result = await job_query.get_job_details_by_id(session, job_id)
        if result:
            return JobFullDetails(**result)
    except Exception as error:
        raise ApplicationException(error)


async def job_match(
    session: AsyncSession,
    request: Request,
    resume_id: int,
    job_id: Optional[int] = None,
    job_desc_id: Optional[int] = None,
    job_title: Optional[str] = None,
    job_desc_text: Optional[str] = None,
) -> JobMatchResult:
    """
    """
    try:
        if not job_id and not job_desc_id and not job_desc_text:
            raise ApplicationException("Invalid input. Job ID or Job Description is required.", status_code=400)

        user = auth.get_current_user(request)

        # job desc is empty, get job desc from job listing
        if not job_desc_text and job_id:
            job = await job_query.get_job_details_by_id(session, job_id)
            if not job:
                raise ApplicationException("Job does not exist", status_code=400)
            if not job["job_description"]:
                raise ApplicationException("Job doesn't have any description", status_code=400)
            job_title = job["job_title"]
            job_desc_text = job["job_description"]

        # job desc remains empty, get job desc from asset
        if not job_desc_text and job_desc_id:
            job_desc_asset = await asset_query.get_user_asset(session, user.id, job_desc_id, AssetStorageType.JOB_DESC)
            if not job_desc_asset:
                raise ApplicationException("Job description asset does not exist", status_code=400)
            job_title = None
            job_desc_text = file.extract_external_document(job_desc_asset["url"])

        # raise exception, cannot calculate similarity score for an empty job desc
        if not job_desc_text:
            raise ApplicationException("Job desc should not be empty", status_code=400)

        # check if job match ever executed previously
        job_match = await job_query.get_job_match_by_content(session, user.id, resume_id, job_desc_text)
        if job_match:
            return JobMatchResult(
                job_match_id=job_match["id"],
                resume_id=resume_id,
                score=job_match["score"],
                job_id=job_match["job_id"],
                job_desc_id=job_match["job_desc_id"],
                job_title=job_title,
                job_desc_text=job_desc_text,
                created_at=job_match["created_at"],
            )

        # extract content from resume
        resume_asset = await asset_query.get_user_asset(session, user.id, resume_id, AssetStorageType.RESUME)
        if not resume_asset:
            raise ApplicationException("Resume asset does not exist", status_code=400)
        resume_text = file.extract_external_document(resume_asset["url"])

        # calculate score
        score = matcher.calculate_cosine_similarity_score(resume_text, job_desc_text)

        # insert job match
        job_match_id = await job_query.insert_job_match(
            session,
            user.id,
            job_id,
            resume_id,
            job_desc_id,
            job_title,
            job_desc_text,
            score
        )

        # wrap result
        return JobMatchResult(
            job_match_id=job_match_id,
            resume_id=resume_id,
            score=score,
            job_id=job_id,
            job_desc_id=job_desc_id,
            job_title=job_title,
            job_desc_text=job_desc_text,
            created_at=dt.datetime.now(dt.UTC),
        )

    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(f"failed to match job due to {error}", error=error)


async def job_match_with_file(
    session: AsyncSession,
    request: Request,
    resume_id: int,
    job_desc_file: UploadFile
) -> JobMatchResult:
    """
    """
    try:
        with file.UploadFileHandler() as handler:
            filepath = handler.temp_local_write(job_desc_file)
            job_desc_text = file.extract_document(filepath)
            return await job_match(session, request, resume_id, job_desc_text=job_desc_text)
    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(f"failed to match job due to {error}", error=error)


async def job_match_with_files(
    session: AsyncSession,
    request: Request,
    resume_file: UploadFile,
    job_desc_file: UploadFile
) -> JobMatchResult:
    """
    """
    try:
        user = auth.get_current_user(request)
        with file.UploadFileHandler() as handler:

            # upload resume
            filepath = handler.temp_local_write(resume_file)
            resume_filename = filepath.split("/")[-1]
            key = f"resume/{user.hash}/{resume_filename}"
            asset_url = s3.upload_file(key, filepath)

            # insert resume
            resume_id = await asset_query.insert_asset(session, user.id, asset_url, AssetStorageType.RESUME)

            # extract job desc
            filepath = handler.temp_local_write(job_desc_file)
            job_desc_text = file.extract_document(filepath)
        return await job_match(session, request, resume_id, job_desc_text=job_desc_text)
    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(f"failed to match job due to {error}", error=error)


async def get_job_match_history(
    session: AsyncSession,
    request: Request,
    page: int,
    row: int
) -> List[JobMatchResult]:
    try:
        user = auth.get_current_user(request)
        job_match_list = await job_query.get_job_match_history(session, user.id, page, row)

        return [
            JobMatchResult(
                job_match_id=job_match["id"],
                resume_id=job_match["resume_id"],
                score=job_match["score"],
                job_id=job_match["job_id"],
                job_desc_id=job_match["job_desc_id"],
                job_desc_text=job_match["job_desc_text"],
                created_at=job_match["created_at"],
            )
            for job_match in job_match_list
        ]

    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(f"failed to get job match history due to {error}", error=error)


async def analyze_job_match(
    session: AsyncSession,
    request: Request,
    job_match_id: int
) -> bool:
    """
    """
    try:
        # get job match
        user = auth.get_current_user(request)
        job_match = await job_query.get_job_match(session, user.id, job_match_id)
        if not job_match:
            raise ApplicationException("Job Match not found", status_code=400)

        # get current job analysis
        job_analysis = await analysis_query.get_analysis(session, user.id, job_match_id)
        if job_analysis:
            match job_analysis["status_code"]:
                # return immediately, no need to re-run the OpenAI to save cost
                case JobAnalysisStatus.SUCCESS:
                    return True

                # re-send task to job worker
                case JobAnalysisStatus.FAILED_RETRYABLE:
                    pass

                # return immediately because we cannot re-run the non retryable to save cost
                case JobAnalysisStatus.FAILED_NON_RETRYABLE:
                    return False

        # get resume content
        resume_asset = await asset_query.get_user_asset(session, user.id, job_match["resume_id"], AssetStorageType.RESUME)
        if not resume_asset:
            raise ApplicationException("Resume asset does not exist", status_code=400)

        # get job desc content
        job_title = job_match["job_title"]
        job_desc_text = job_match["job_desc_text"]

        # get job details if exist
        job_company = None
        job = await job_query.get_job_details_by_id(session, job_match["job_id"])
        if job:
            job_title = job["job_title"]
            job_company = job["company_name"]

        # send task to job worker
        analyze_task.start_job_match_analysis.delay(
            job_match_id,
            job_desc_text,
            job_title,
            job_company,
            resume_asset["url"],
        )

        return True

    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(error)


async def get_job_analysis_result(
    session: AsyncSession,
    request: Request,
    job_match_id: int
) -> Optional[JobMatchAnalysisResult]:
    """
    """
    try:
        user = auth.get_current_user(request)
        result = await analysis_query.get_analysis(session, user.id, job_match_id)
        if result:
            return JobMatchAnalysisResult(
                analysis_id=result["id"],
                created_at=result["created_at"],
                status_code=result["status_code"],
                score=result["score"],
                asset_type=result["asset_type"],
                asset_url=result["asset_url"],
            )
    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(error)
