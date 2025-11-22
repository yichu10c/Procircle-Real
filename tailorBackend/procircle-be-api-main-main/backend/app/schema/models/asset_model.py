"""
Asset Database Model
"""
import datetime as dt

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from app.schema.models.user_model import GuestUser
from app.tools.sql import Base


class Asset(Base):
    __tablename__ = "asset"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    url = Column(String(256), nullable=False)
    type = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: dt.datetime.now(dt.UTC), nullable=False)


class UserAsset(Base):
    __tablename__ = "user_asset"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    asset_id = Column(Integer, ForeignKey(Asset.id), nullable=False)
    user_id = Column(Integer, ForeignKey(GuestUser.id), nullable=False)
