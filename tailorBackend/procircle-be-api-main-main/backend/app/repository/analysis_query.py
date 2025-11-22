"""
Analysis Query
"""
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.models.asset_model import Asset
from app.schema.models.job_model import JobMatch, JobMatchAnalysis
from app.schema.models.user_model import GuestUser
from app.tools.sql.query_wrapper import as_dict, within


async def get_analysis(
    session: AsyncSession,
    user_id: int,
    job_match_id: int
) -> Dict[str, Any]:
    """
    """
    result = await (
        within(session)
        .select(
            JobMatchAnalysis.id,
            JobMatchAnalysis.created_at,
            JobMatchAnalysis.status_code,
            JobMatch.score,
            Asset.type.label("asset_type"),
            Asset.url.label("asset_url"),
        ).join(
            JobMatch,
            JobMatch.id == JobMatchAnalysis.job_match_id
        ).join(
            Asset,
            Asset.id == JobMatchAnalysis.result_asset_id
        ).join(
            GuestUser,
            GuestUser.id == JobMatch.user_id
        ).where(
            JobMatchAnalysis.job_match_id == job_match_id,
            GuestUser.id == user_id
        ).first()
    )

    return as_dict(result)


async def upsert_analysis(
    session: AsyncSession,
    job_match_id: int,
    result_asset_id: int,
    status: int,
) -> int:
    """
    """
    # check current analysis
    analysis = await (
        within(session)
        .select(JobMatchAnalysis)
        .where(JobMatchAnalysis.job_match_id == job_match_id)
        .first()
    )

    # update if any
    if analysis:
        return await (
            within(session)
            .update(JobMatchAnalysis)
            .values({
                JobMatchAnalysis.job_match_id: job_match_id,
                JobMatchAnalysis.result_asset_id: result_asset_id,
                JobMatchAnalysis.status_code: status
            })
            .update_row()
        )

    # else insert instead
    return await (
        within(session)
        .insert(JobMatchAnalysis)
        .values({
            JobMatchAnalysis.job_match_id: job_match_id,
            JobMatchAnalysis.result_asset_id: result_asset_id,
            JobMatchAnalysis.status_code: status
        })
        .insert_row()
    )


async def delete_analysis(
    session: AsyncSession,
    job_match_id: int,
) -> bool:
    """
    """
    res = await (
        within(session)
        .delete(JobMatchAnalysis)
        .where(JobMatchAnalysis.job_match_id == job_match_id)
        .delete_row()
    )

    return bool(res)
