import asyncio
from job_worker.core import app
from job_worker.controller import analyze_controller


@app.task
def start_job_match_analysis(
    job_match_id: int,
    job_desc_text: str,
    job_title: str,
    job_company: str,
    resume_url: str,
):
    """
    Start Job Match Analysis using OpenAI

    analysis_asset_id behavior:
    - asset id == -1 non retryable
    - asset id == 0 retryable
    - asset id > 0 success
    """
    asyncio.run(
        analyze_controller.handle_job_match_analysis(
            job_match_id=job_match_id,
            job_desc_text=job_desc_text,
            job_title=job_title,
            job_company=job_company,
            resume_url=resume_url,
        )
    )


@app.task
def start_job_match_analysis_wpa(job_match_id: int):
    """
    Start Job Match Analysis WPA using OpenAI

    analysis_asset_id behavior:
    - asset id == -1 non retryable
    - asset id == 0 retryable
    - asset id > 0 success
    """
    asyncio.run(
        analyze_controller.handle_job_match_analysis_wpa(
            job_match_id=job_match_id
        )
    )


@app.task
def start_linkedin_profile_analysis(profile_id: int, profile_data: dict, job_types: str):
    """Start LinkedIn profile analysis"""
    asyncio.run(
        analyze_controller.handle_linkedin_profile_analysis(
            profile_id=profile_id,
            profile_data=profile_data,
            job_types=job_types,
        )
    )
