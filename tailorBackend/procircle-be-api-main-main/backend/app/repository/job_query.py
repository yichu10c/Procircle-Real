"""
Job Query
"""
from typing import Any, Dict, List, Optional

from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.models.job_model import Job, JobMatch
from app.schema.models.user_model import GuestUser
from app.schema.data.job import JobShortDetailsItem, JobFullDetails
from app.tools.sql.query_wrapper import as_dict, within


async def get_job_list(
    session: AsyncSession,
    page: int,
    row: int
) -> List[JobShortDetailsItem]:
    """
    """
    result = await (
        within(session)
        .select(
            Job.id,
            Job.updated_at,
            Job.job_title,
            Job.company_name,
            Job.industries,
            Job.location,
            Job.seniority_level
        ).limit(
            row
        ).offset(
            (page - 1) * row
        ).all()
    )

    return [JobShortDetailsItem(**res) for res in as_dict(result)]


async def get_job_details_by_id(
    session: AsyncSession,
    job_id: int
) -> JobFullDetails:
    """
    """
    result = await (
        within(session)
        .select(
            Job.id,
            Job.created_at,
            Job.updated_at,
            Job.job_title,
            Job.company_name,
            Job.company_link,
            Job.job_description,
            Job.seniority_level,
            Job.employment_type,
            Job.job_function,
            Job.industries,
            Job.location,
            Job.logo,
        ).where(
            Job.id == job_id
        ).first()
    )

    return as_dict(result)


async def get_job_match(
    session: AsyncSession,
    user_id: int,
    job_match_id: int,
) -> Dict[str, Any]:
    """
    Used to get job match which are belongs to specified user id,
    this function has a natural validation through database query
    """
    result = await (
        within(session)
        .select(JobMatch)
        .where(
            JobMatch.user_id == user_id,
            JobMatch.id == job_match_id,
        )
        .first()
    )
    return as_dict(result)


async def get_job_match_by_content(
    session: AsyncSession,
    user_id: int,
    resume_id: int,
    job_desc_text: str
) -> Dict[str, Any]:
    """
    """
    result = await (
        within(session)
        .select(JobMatch)
        .where(
            JobMatch.user_id == user_id,
            JobMatch.resume_id == resume_id,
            JobMatch.job_desc_text == job_desc_text
        )
        .first()
    )
    return as_dict(result)


async def get_job_match_detailed_user(
    session: AsyncSession,
    job_match_id: int,
) -> Dict[str, Any]:
    """
    Intentionally used for internal only and not for user-facing request
    """
    result = await (
        within(session)
        .select(
            JobMatch.id,
            JobMatch.score,
            JobMatch.job_id,
            JobMatch.resume_id,
            JobMatch.job_title,
            JobMatch.job_desc_text.label("job_desc"),
            GuestUser.id.label("user_id"),
            GuestUser.hash.label("user_hash"),
        )
        .join(
            GuestUser,
            GuestUser.id == JobMatch.user_id
        )
        .where(JobMatch.id == job_match_id)
        .first()
    )
    return as_dict(result)


async def get_job_match_history(
    session: AsyncSession,
    user_id: int,
    page: int,
    row: int
) -> List[Dict[str, Any]]:
    """
    """
    result = await (
        within(session)
        .select(JobMatch)
        .where(JobMatch.user_id == user_id)
        .order_by(desc(JobMatch.created_at))
        .limit(row)
        .offset((page - 1) * row)
        .all()
    )

    return as_dict(result)


async def get_job_match_by_user_resume_jobdesc(
    session: AsyncSession,
    user_id: int,
    resume_id: int,
    job_desc: str
) -> Dict[str, Any]:
    result = await (
        within(session)
        .select(JobMatch)
        .where(
            JobMatch.user_id == user_id,
            JobMatch.resume_id == resume_id,
            JobMatch.job_desc_text == job_desc
        ).first()
    )
    return as_dict(result)


async def insert_job_match(
    session: AsyncSession,
    user_id: int,
    job_id: Optional[int] = None,
    resume_id: Optional[int] = None,
    job_desc_id: Optional[int] = None,
    job_title: Optional[str] = None,
    job_desc_text: Optional[str] = None,
    score: Optional[float] = None,
) -> int:
    """
    """
    return await (
        within(session)
        .insert(JobMatch)
        .values({
            JobMatch.user_id: user_id,
            JobMatch.job_id: job_id,
            JobMatch.resume_id: resume_id,
            JobMatch.job_desc_id: job_desc_id,
            JobMatch.job_title: job_title,
            JobMatch.job_desc_text: job_desc_text,
            JobMatch.score: score
        })
        .insert_row()
    )


async def update_job_match_score(
    session: AsyncSession,
    job_match_id: int,
    score: float
) -> bool:
    return await (
        within(session)
        .update(JobMatch)
        .values({JobMatch.score: score})
        .where(JobMatch.id == job_match_id)
        .update_row()
    )
