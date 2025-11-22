"""
LinkedIn Profile Data
"""
import datetime as dt
from pydantic import BaseModel, field_validator
from typing import Optional

from app.schema.data.asset import AssetStorageType


class LinkedInProfileResult(BaseModel):
    analysis_id: int
    created_at: dt.datetime
    status_code: int
    asset_type: AssetStorageType | str
    asset_url: str

    @field_validator("asset_type")
    def validate_asset_type(cls, value: AssetStorageType | str):
        if isinstance(value, AssetStorageType):
            return value
        return getattr(AssetStorageType, value)


class AnalyzeLinkedInProfileResult(BaseModel):
    profile_id: int
