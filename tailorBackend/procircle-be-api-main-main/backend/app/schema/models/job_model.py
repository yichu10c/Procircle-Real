"""
Job Database Model
"""
import datetime as dt
from sqlalchemy import Column, Float, ForeignKey, Integer, DateTime, String, Text

from app.schema.models.asset_model import Asset
from app.schema.models.user_model import GuestUser
from app.tools.sql import Base


class Job(Base):
    __tablename__ = "linkedin_jobs"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    job_id = Column(Text, index=True)
    job_title = Column(Text, nullable=True)
    job_linkedin_url = Column(Text, nullable=True)
    company_name = Column(Text, nullable=True)
    company_link = Column(Text, nullable=True)
    date_of_listing = Column(Text, nullable=True)
    job_description = Column(Text, nullable=True)
    seniority_level = Column(Text, nullable=True)
    employment_type = Column(Text, nullable=True)
    job_function = Column(Text, nullable=True)
    industries = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    logo = Column(Text, nullable=True)


class JobMatch(Base):
    __tablename__ = "job_match"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey(GuestUser.id), nullable=False)
    job_id = Column(Integer, ForeignKey(Job.id), default=None, nullable=True)
    resume_id = Column(Integer, ForeignKey(Asset.id), default=None, nullable=True)
    job_desc_id = Column(Integer, ForeignKey(Asset.id), default=None, nullable=True)
    job_title = Column(String(256), default=None, nullable=True)
    job_desc_text = Column(Text, default=None, nullable=True)
    score = Column(Float, default=None, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: dt.datetime.now(dt.UTC))


class JobMatchAnalysis(Base):
    __tablename__ = "job_match_analysis"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    job_match_id = Column(Integer, ForeignKey(JobMatch.id), nullable=False, unique=True)
    result_asset_id = Column(Integer, ForeignKey(Asset.id), nullable=True)
    status_code = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: dt.datetime.now(dt.UTC), nullable=False)
