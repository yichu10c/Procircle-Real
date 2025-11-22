"""
Asset Service
"""
from typing import Any, Dict

from app.schema.data.asset import AssetStorageType
from app.repository import asset_query
from app.tools.sql import connection


class AssetService:
    async def get_asset(self, user_id: int, asset_id: int) -> Dict[str, Any]:
        """
        Get asset
        """
        async with connection.async_session() as sess:
            return await asset_query.get_asset_by_id(sess, user_id, asset_id)

    async def insert_asset(self, user_id: int, asset_url: str, asset_type: str) -> int:
        """
        Insert asset
        """
        async with connection.async_session() as sess:
            return await asset_query.insert_asset(
                sess, user_id, asset_url, getattr(AssetStorageType, asset_type)
            )
