from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.repository import li_profile_query, user_query
from app.schema.data.asset import AssetStorageType
from app.schema.data.li_profile import LinkedInProfileResult, AnalyzeLinkedInProfileResult
from app.tools.security import auth
from job_worker.task import analyze_task
from app.utils.exceptions import ApplicationException


async def analyze_profile(
    session: AsyncSession,
    profile_data: dict,
    job_types: str,
    wp_user_id: int,
) -> AnalyzeLinkedInProfileResult:
    try:
        user_hash = auth.generate_user_hash()
        user_id = await user_query.insert_user(session, user_hash)
        profile_json = json.dumps(profile_data)
        profile_id = await li_profile_query.insert_profile(
            session, user_id, profile_json, job_types, wp_user_id
        )
        analyze_task.start_linkedin_profile_analysis.delay(
            profile_id, profile_data, job_types
        )
        return AnalyzeLinkedInProfileResult(profile_id=profile_id)
    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(error)


async def get_profile_analysis(
    session: AsyncSession,
    profile_id: int,
    wp_user_id: int,
) -> LinkedInProfileResult | None:
    try:
        result = await li_profile_query.get_profile_analysis(
            session, profile_id, wp_user_id
        )
        if result:
            return LinkedInProfileResult(
                analysis_id=result["id"],
                created_at=result["created_at"],
                status_code=result["status_code"],
                asset_type=result.get("asset_type", AssetStorageType.ANALYSIS),
                asset_url=result.get("asset_url", ""),
            )
    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(error)
