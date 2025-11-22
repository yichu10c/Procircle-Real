"""
Asset View
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.v1 import asset_controller
from app.schema.data.asset import AssetStorageType
from app.schema.request.asset_request import GetPresignedURLSpec, InsertAssetSpec
from app.schema.response.asset_response import (
    GenerateAssetPresignedURLResponse, GetAssetStorage, GetAssetStorageList,
    InsertAssetResponse, InsertAssetResult, AssetStorageItem
)
from app.tools.security import auth
from app.tools.sql import connection


router = APIRouter(
    prefix="/assets",
    dependencies=[Depends(auth.api_authentication)]
)

@router.post("/presigned_url")
async def generate_presigned_url(
    spec: GetPresignedURLSpec,
    request: Request
) -> GenerateAssetPresignedURLResponse:
    """
    """
    result = await asset_controller.get_presigned_url(spec.asset_type, spec.asset_name, request)
    return GenerateAssetPresignedURLResponse(data=result)


@router.post("/storage")
async def insert_storage_item(
    request: Request,
    spec: InsertAssetSpec,
    session: AsyncSession = Depends(connection.get_session)
) -> InsertAssetResponse:
    """
    """
    result = await asset_controller.insert_asset_to_storage(
        request, session, spec.url, spec.asset_type
    )
    return InsertAssetResponse(
        data=InsertAssetResult(
            asset_id=result,
            status=bool(result)
        )
    )


@router.get("/storage")
async def get_storage_items(
    request: Request,
    asset_type: AssetStorageType,
    session: AsyncSession = Depends(connection.get_session)
) -> GetAssetStorageList:
    """
    """
    result = await asset_controller.get_asset_storage_items(
        request, session, asset_type
    )

    return GetAssetStorageList(
        data=[
            AssetStorageItem(
                asset_id=res["id"],
                url=res["url"],
                type=res["type"],
                created_at=res["created_at"],
            ) for res in result
        ]
    )


@router.get("/storage/{asset_id}")
async def get_storage_item(
    request: Request,
    asset_id: int,
    session: AsyncSession = Depends(connection.get_session)
) -> GetAssetStorage:
    """
    """
    result = await asset_controller.get_asset_storage_items_by_id(request, session, asset_id)
    if result:
        return GetAssetStorage(
            data=AssetStorageItem(
                asset_id=result["id"],
                url=result["url"],
                type=result["type"],
                created_at=result["created_at"],
            )
        )
    else:
        return GetAssetStorage()
