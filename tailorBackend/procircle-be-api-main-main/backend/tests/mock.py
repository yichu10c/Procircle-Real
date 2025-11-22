import datetime as dt

from sqlalchemy.sql import delete
from sqlalchemy.orm.session import Session

from app.schema.models.asset_model import Asset, UserAsset
from app.schema.models.job_model import Job, JobMatch, JobMatchAnalysis
from app.schema.models.li_profile_model import LinkedInProfile, LinkedInProfileAnalysis
from app.schema.models.user_model import GuestUser
from app.tools.security import auth


def remove_all_mocks(session: Session):
    session.execute(delete(LinkedInProfileAnalysis))
    session.execute(delete(LinkedInProfile))
    session.execute(delete(JobMatchAnalysis))
    session.execute(delete(JobMatch))
    session.execute(delete(Job))
    session.execute(delete(UserAsset))
    session.execute(delete(Asset))
    session.execute(delete(GuestUser))
    session.commit()


def create_dummy_user(session: Session):
    user_hash = auth.generate_user_hash()
    user = GuestUser(
        hash=user_hash,
    )
    session.add(user)
    session.commit()
    user.token = auth.generate_session_token(user_hash)
    return user


def create_dummy_job(session: Session) -> Job:
    job = Job(
        created_at=dt.datetime.now(),
        updated_at=dt.datetime.now(),
        deleted_at=None,
        job_title="Software Engineer",
        job_linkedin_url="",
        company_name="Google",
        company_link="google.com",
        date_of_listing="",
        job_description="craft software",
        seniority_level="entry level",
        employment_type="",
        job_function="",
        industries="Software",
        location="USA",
        logo="",
    )
    session.add(job)
    session.commit()
    return job


def create_dummy_resume(session: Session, user_id: int):
    """
    Resumes:
    - https://procircle.s3.us-east-2.amazonaws.com/public/20240729EthanHuResume.docx
    - https://procircle.s3.us-east-2.amazonaws.com/public/Michael+Tung+For+Testing.docx
    """
    resume_asset = Asset(
        url="https://procircle.s3.us-east-2.amazonaws.com/public/20240729EthanHuResume.docx",
        type="RESUME",
        created_at=dt.datetime.now(),
    )
    session.add(resume_asset)
    session.commit()
    user_asset = UserAsset(
        asset_id=resume_asset.id,
        user_id=user_id,
    )
    session.add(user_asset)
    session.commit()
    return resume_asset


def create_dummy_job_desc(session: Session, user_id: int):
    """
    Job Desc:
    - JD: https://procircle.s3.us-east-2.amazonaws.com/public/ProCircle-JD+Sample.docx
    """
    job_desc_asset = Asset(
        url="https://procircle.s3.us-east-2.amazonaws.com/public/ProCircle-JD+Sample.docx",
        type="JOB_DESC",
        created_at=dt.datetime.now(),
    )
    session.add(job_desc_asset)
    session.commit()
    user_asset = UserAsset(
        asset_id=job_desc_asset.id,
        user_id=user_id,
    )
    session.add(user_asset)
    session.commit()
    return job_desc_asset


def create_dummy_analysis_result(session: Session, user_id: int):
    """
    Job Desc:
    - JD: https://procircle.s3.us-east-2.amazonaws.com/public/ProCircle-JD+Sample.docx
    """
    analysis_asset = Asset(
        url="https://procircle.s3.us-east-2.amazonaws.com/public/ProCircle-JD+Sample.docx",
        type="ANALYSIS",
        created_at=dt.datetime.now(),
    )
    session.add(analysis_asset)
    session.commit()
    user_asset = UserAsset(
        asset_id=analysis_asset.id,
        user_id=user_id,
    )
    session.add(user_asset)
    session.commit()
    return analysis_asset


def create_dummy_job_match(
    session: Session,
    user_id: int,
    resume_id: int,
    job_id: int,
    job_desc_id: int,
):
    job_match = JobMatch(
        user_id=user_id,
        job_id=job_id,
        resume_id=resume_id,
        job_desc_id=job_desc_id,
        job_desc_text="",
        score=1,
    )
    session.add(job_match)
    session.commit()
    return job_match


def create_dummy_job_match_analysis(
    session: Session, job_match_id: int, result_asset_id: int
):
    job_match_analysis = JobMatchAnalysis(
        job_match_id=job_match_id, result_asset_id=result_asset_id
    )
    session.add(job_match_analysis)
    session.commit()
    return job_match_analysis


def create_dummy_profile(session: Session, user_id: int, wp_user_id: int = 1) -> LinkedInProfile:
    profile = LinkedInProfile(
        user_id=user_id, wp_user_id=wp_user_id, profile_data="{}", job_types="software"
    )
    session.add(profile)
    session.commit()
    return profile


def create_dummy_profile_analysis(
    session: Session, profile_id: int, result_asset_id: int, wp_user_id: int = 1
) -> LinkedInProfileAnalysis:
    analysis = LinkedInProfileAnalysis(
        profile_id=profile_id,
        result_asset_id=result_asset_id,
        status_code=1,
        wp_user_id=wp_user_id,
    )
    session.add(analysis)
    session.commit()
    return analysis
