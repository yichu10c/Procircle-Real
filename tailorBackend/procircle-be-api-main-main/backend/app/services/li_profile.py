"""
LinkedIn Profile Service
"""

from typing import Dict, Any

from app.repository import li_profile_query
from app.tools.sql import connection


class ProfileService:
    async def get_profile_details(self, profile_id: int) -> Dict[str, Any]:
        async with connection.async_session() as sess:
            return await li_profile_query.get_profile_details(sess, profile_id)

    async def upsert_analysis(
        self, profile_id: int, result_asset_id: int, status: int, wp_user_id: int
    ) -> int:
        async with connection.async_session() as sess:
            return await li_profile_query.upsert_profile_analysis(
                sess, profile_id, result_asset_id, status, wp_user_id
            )
