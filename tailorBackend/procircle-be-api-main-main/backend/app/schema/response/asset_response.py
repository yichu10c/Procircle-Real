"""
Asset Response
"""
from pydantic import BaseModel
from typing import List, Optional

from app.schema.data.asset import AssetStorageItem, AssetPresignedURL
from app.schema.response import BaseResponseSchema


class GenerateAssetPresignedURLResponse(BaseResponseSchema):
    data: Optional[AssetPresignedURL]


class GetAssetStorageList(BaseResponseSchema):
    data: List[AssetStorageItem]


class GetAssetStorage(BaseResponseSchema):
    data: Optional[AssetStorageItem] = None


class InsertAssetResult(BaseModel):
    asset_id: int
    status: bool


class InsertAssetResponse(BaseResponseSchema):
    data: InsertAssetResult
