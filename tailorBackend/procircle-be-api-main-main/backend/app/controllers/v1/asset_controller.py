import httpx
from uuid import uuid4
from typing import Any, Dict, List, Optional

from fastapi import Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.data.asset import AssetStorageItem, AssetStorageType, AssetPresignedURL
from app.repository import asset_query
from tools.aws import s3
from tools.observability.log import get_logger
from app.tools.resource import file
from app.tools.security import auth
from app.utils.exceptions import ApplicationException


async def get_presigned_url(
    asset_type: AssetStorageType,
    asset_name: str,
    request: Request
) -> AssetPresignedURL:
    """
    """
    logger = await get_logger(request)
    try:
        user = auth.get_current_user(request)
        key = f"{asset_type.value.lower()}/{user.hash}/{asset_name}".replace(" ", "+")
        download_url, upload_url = s3.get_download_upload_presigned_url(key)

        return AssetPresignedURL(download_url=download_url, upload_url=upload_url)

    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        logger.error(f"failed to get storage presigned url.")
        raise ApplicationException(
            message=str(error),
            error=error
        )


async def get_asset_storage_items(
    request: Request,
    session: AsyncSession,
    asset_type: AssetStorageType
) -> List[Dict[str, Any]]:
    """
    """
    try:
        user = auth.get_current_user(request)
        return await asset_query.get_asset_by_type(
            session, user.id, asset_type
        )

    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(
            message=f"failed to get storage items. {asset_type=}. {error=}",
            error=error
        )


async def get_asset_storage_items_by_id(
    request: Request,
    session: AsyncSession,
    asset_id: int,
) -> Dict[str, Any]:
    """
    """
    try:
        user = auth.get_current_user(request)
        return await asset_query.get_asset_by_id(session, user.id, asset_id)

    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(
            message=f"failed to get storage items. {error=}",
            error=error
        )


async def insert_asset_to_storage(
    request: Request,
    session: AsyncSession,
    url: str,
    asset_type: AssetStorageType,
) -> int:
    """
    """
    try:
        user = auth.get_current_user(request)
        return await asset_query.insert_asset(session, user.id, url, asset_type)

    except Exception as error:
        if isinstance(error, ApplicationException):
            raise error
        raise ApplicationException(
            message=f"failed to insert asset storage items. {asset_type=}. {error=}",
            error=error
        )
