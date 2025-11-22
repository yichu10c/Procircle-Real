"""
LinkedIn Profile Queries
"""

from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.models.li_profile_model import LinkedInProfile, LinkedInProfileAnalysis
from app.schema.models.user_model import GuestUser
from app.schema.models.asset_model import Asset
from app.schema.data.asset import AssetStorageType
from app.tools.sql.query_wrapper import as_dict, within


async def insert_profile(
    session: AsyncSession,
    user_id: int,
    profile_data: str,
    job_types: str,
    wp_user_id: int | None = None,
) -> int:
    return await (
        within(session)
        .insert(LinkedInProfile)
        .values({
            LinkedInProfile.user_id: user_id,
            LinkedInProfile.wp_user_id: wp_user_id,
            LinkedInProfile.profile_data: profile_data,
            LinkedInProfile.job_types: job_types,
        })
        .insert_row()
    )


async def get_profile_details(
    session: AsyncSession,
    profile_id: int,
) -> Dict[str, Any]:
    result = await (
        within(session)
        .select(
            LinkedInProfile.id,
            LinkedInProfile.profile_data,
            LinkedInProfile.job_types,
            LinkedInProfile.wp_user_id,
            GuestUser.id.label("user_id"),
            GuestUser.hash.label("user_hash"),
        )
        .join(GuestUser, GuestUser.id == LinkedInProfile.user_id)
        .where(LinkedInProfile.id == profile_id)
        .first()
    )
    return as_dict(result)


async def upsert_profile_analysis(
    session: AsyncSession,
    profile_id: int,
    result_asset_id: int,
    status: int,
    wp_user_id: int | None = None,
) -> int:
    analysis = await (
        within(session)
        .select(LinkedInProfileAnalysis)
        .where(LinkedInProfileAnalysis.profile_id == profile_id)
        .first()
    )
    if analysis:
        return await (
            within(session)
            .update(LinkedInProfileAnalysis)
            .values({
                LinkedInProfileAnalysis.profile_id: profile_id,
                LinkedInProfileAnalysis.result_asset_id: result_asset_id,
                LinkedInProfileAnalysis.status_code: status,
                LinkedInProfileAnalysis.wp_user_id: wp_user_id,
            })
            .update_row()
        )
    return await (
        within(session)
        .insert(LinkedInProfileAnalysis)
        .values({
            LinkedInProfileAnalysis.profile_id: profile_id,
            LinkedInProfileAnalysis.result_asset_id: result_asset_id,
            LinkedInProfileAnalysis.status_code: status,
            LinkedInProfileAnalysis.wp_user_id: wp_user_id,
        })
        .insert_row()
    )


async def get_profile_analysis(
    session: AsyncSession,
    profile_id: int,
    wp_user_id: int,
) -> Dict[str, Any]:
    result = await (
        within(session)
        .select(
            LinkedInProfileAnalysis.id,
            LinkedInProfileAnalysis.created_at,
            LinkedInProfileAnalysis.status_code,
            Asset.type.label("asset_type"),
            Asset.url.label("asset_url"),
        )
        .join(LinkedInProfile, LinkedInProfile.id == LinkedInProfileAnalysis.profile_id)
        .outerjoin(Asset, Asset.id == LinkedInProfileAnalysis.result_asset_id)
        .where(
            LinkedInProfileAnalysis.profile_id == profile_id,
            LinkedInProfile.wp_user_id == wp_user_id,
        )
        .first()
    )
    return as_dict(result)
