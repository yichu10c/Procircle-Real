import datetime as dt
from sqlalchemy import Column, ForeignKey, Integer, Text, DateTime

from app.schema.models.user_model import GuestUser
from app.schema.models.asset_model import Asset
from app.tools.sql import Base


class LinkedInProfile(Base):
    __tablename__ = "linkedin_profiles"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey(GuestUser.id), nullable=False)
    wp_user_id = Column(Integer, nullable=True, index=True)
    profile_data = Column(Text, nullable=False)
    job_types = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: dt.datetime.now(dt.UTC))


class LinkedInProfileAnalysis(Base):
    __tablename__ = "linkedin_match_analysis"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    profile_id = Column(Integer, ForeignKey(LinkedInProfile.id), unique=True, nullable=False)
    wp_user_id = Column(Integer, nullable=True, index=True)
    result_asset_id = Column(Integer, ForeignKey(Asset.id), nullable=True)
    status_code = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: dt.datetime.now(dt.UTC), nullable=False)
