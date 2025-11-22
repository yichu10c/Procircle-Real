"""
Asset Query
"""
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.models.asset_model import Asset, UserAsset
from app.schema.data.asset import AssetStorageItem, AssetStorageType
from app.tools.sql.query_wrapper import as_dict, within


async def get_asset_by_type(
    session: AsyncSession,
    user_id: int,
    asset_type: AssetStorageType
) -> List[AssetStorageItem]:
    """
    """
    result = await (
        within(session)
        .select(Asset)
        .join(
            UserAsset,
            UserAsset.asset_id == Asset.id
        ).where(
            UserAsset.user_id == user_id,
            Asset.type == asset_type.value
        ).all()
    )

    return as_dict(result)


async def get_asset_by_id(
    session: AsyncSession,
    user_id: int,
    asset_id: int,
) -> List[AssetStorageItem]:
    """
    """
    result = await (
        within(session)
        .select(Asset)
        .join(
            UserAsset,
            UserAsset.asset_id == Asset.id
        ).where(
            UserAsset.user_id == user_id,
            UserAsset.asset_id == asset_id
        ).first()
    )

    return as_dict(result)


async def insert_asset(
    session: AsyncSession,
    user_id: int,
    url: str,
    asset_type: AssetStorageType
) -> int :
    """
    """
    asset_id = await (
        within(session)
        .insert(Asset)
        .values({
            Asset.url: url,
            Asset.type: asset_type.value
        })
        .insert_row()
    )
    if not asset_id:
        return 0

    user_asset_id = await (
        within(session)
        .insert(UserAsset)
        .values({
            UserAsset.asset_id: asset_id,
            UserAsset.user_id: user_id
        })
        .insert_row()
    )
    if not user_asset_id:
        return 0

    return asset_id


async def get_user_asset(
    session: AsyncSession,
    user_id: int,
    asset_id: int,
    asset_type: AssetStorageType
):
    """
    """
    asset = await (
        within(session)
        .select(Asset)
        .join(
            UserAsset,
            UserAsset.asset_id == Asset.id
        ).where(
            UserAsset.user_id == user_id,
            UserAsset.asset_id == asset_id,
            Asset.type == asset_type.value
        ).first()
    )

    return as_dict(asset)
