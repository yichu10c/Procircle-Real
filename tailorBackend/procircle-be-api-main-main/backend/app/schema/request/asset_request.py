"""
Asset Request Spec
"""
from pydantic import BaseModel

from app.schema.data.asset import AssetStorageType


class GetPresignedURLSpec(BaseModel):
    asset_type: AssetStorageType
    asset_name: str


class InsertAssetSpec(BaseModel):
    asset_type: AssetStorageType
    url: str
