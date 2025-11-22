"""
Asset Data
"""
import datetime as dt
import enum
from pydantic import BaseModel
from typing import List, Optional


class AssetStorageType(str, enum.Enum):
    RESUME = "RESUME"
    JOB_DESC = "JOB_DESC"
    ANALYSIS = "ANALYSIS"
    LI_PROFILE = "LI_PROFILE"


class AssetPresignedURL(BaseModel):
    download_url: str
    upload_url: str


class AssetStorageItem(BaseModel):
    asset_id: int
    url: str
    type: AssetStorageType
    created_at: dt.datetime
