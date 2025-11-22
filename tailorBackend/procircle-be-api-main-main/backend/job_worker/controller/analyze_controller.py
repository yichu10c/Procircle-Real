import datetime as dt
from openai import OpenAIError
import os
import json

from app.services import asset_service, job_service, profile_service
from job_worker.tools import file, profile as profile_tool
from job_worker.constant import JobAnalysisStatus
from job_worker.tools import analyzer
from tools.observability.log import main_logger as logger


async def handle_job_match_analysis(
    job_match_id: int,
    job_desc_text: str,
    job_title: str,
    job_company: str,
    resume_url: str,
):
    """
    Handle Job Match Analysis using OpenAI

    analysis_asset_id behavior:
    - asset id == -1 non retryable
    - asset id == 0 retryable
    - asset id > 0 success
    """
    start_time = dt.datetime.now(dt.UTC).timestamp()
    analysis_asset_id = 0
    status = False

    try:
        logger.info(f"Job analysis start. {job_match_id=}")

        # analyze using OpenAI
        resume_text = file.extract_docx_from_url(resume_url)
        result = await analyzer.analyze_job_match(job_desc_text, resume_text, job_title, job_company)

        # resolve user
        job_match = await job_service.get_job_match_details(job_match_id)

        # convert to pdf and upload result
        download_url = await file.handle_upload_pdf(
            result, job_match["user_hash"], prefix="job-match-analysis"
        )

        # insert result to db
        analysis_asset_id = await asset_service.insert_asset(
            job_match["user_id"], download_url, "ANALYSIS"
        )
        analysis_id = await job_service.upsert_analysis(job_match_id, analysis_asset_id, JobAnalysisStatus.SUCCESS)
        status = bool(analysis_asset_id and analysis_id)

    except OpenAIError as error:
        await job_service.upsert_analysis(job_match_id, None, JobAnalysisStatus.FAILED_NON_RETRYABLE)
        logger.error(f"Job analysis failed during OpenAI client request. {error=}", error)

    except Exception as error:
        await job_service.upsert_analysis(job_match_id, None, JobAnalysisStatus.FAILED_RETRYABLE)
        logger.error(f"Job analysis failed during internal processes. {error=}", error)

    # insert analysis metadata
    finally:
        elapsed = dt.datetime.now(dt.UTC).timestamp() - start_time
        logger.info(f"Job analysis finished. status: {status}. elapsed: {elapsed:.2f}s.")


async def handle_job_match_analysis_wpa(job_match_id: int):
    """
    Handle Job Match Analysis using OpenAI

    analysis_asset_id behavior:
    - asset id == -1 non retryable
    - asset id == 0 retryable
    - asset id > 0 success
    """
    start_time = dt.datetime.now(dt.UTC).timestamp()
    analysis_asset_id = 0
    analysis_id = 0
    update_job_status = 0
    status = False

    try:
        logger.info(f"Job analysis start. {job_match_id=}")

        # get job match
        job_match = await job_service.get_job_match_details(job_match_id)
        if not job_match:
            raise Exception("Job match not found")

        # analyze using OpenAI
        resume = await asset_service.get_asset(
            user_id=job_match["user_id"],
            asset_id=job_match["resume_id"],
        )
        resume_text = file.extract_docx_from_url(resume["url"])
        logger.info("[handle_job_match_analysis_wpa] analyze with openAI")
        result = await analyzer.analyze_job_match_wpa(
            job_title=job_match["job_title"],
            job_desc_text=job_match["job_desc"],
            resume_text=resume_text,
        )

        # resolve user
        logger.info("[handle_job_match_analysis_wpa] get job match details")
        job_match = await job_service.get_job_match_details(job_match_id)

        # convert to pdf and upload result
        logger.info("[handle_job_match_analysis_wpa] upload pdf")
        download_url = await file.handle_upload_pdf(
            result.html_content,
            job_match["user_hash"],
            prefix="job-match-analysis",
        )

        # insert result to db
        logger.info("[handle_job_match_analysis_wpa] updating result")
        analysis_asset_id = await asset_service.insert_asset(
            job_match["user_id"], download_url, "ANALYSIS"
        )
        analysis_id = await job_service.upsert_analysis(job_match_id, analysis_asset_id, JobAnalysisStatus.SUCCESS)
        update_job_status = await job_service.update_job_match_score(job_match_id, result.wpa_score)
        status = bool(analysis_asset_id and analysis_id and update_job_status)

    except OpenAIError as error:
        logger.error(f"Job analysis failed during OpenAI client request. {error=}")
        await job_service.upsert_analysis(job_match_id, None, JobAnalysisStatus.FAILED_NON_RETRYABLE)

    except Exception as error:
        logger.error(f"Job analysis failed during internal processes. {error=}")
        await job_service.upsert_analysis(job_match_id, None, JobAnalysisStatus.FAILED_RETRYABLE)

    # insert analysis metadata
    finally:
        elapsed = dt.datetime.now(dt.UTC).timestamp() - start_time
        logger.info(
            f"Job analysis finished. status: {status}. elapsed: {elapsed:.2f}s. {analysis_asset_id=} {analysis_id=} {update_job_status=}"
        )


async def handle_linkedin_profile_analysis(
    profile_id: int, profile_data: dict, job_types: str
):
    """Handle LinkedIn profile analysis"""
    start_time = dt.datetime.now(dt.UTC).timestamp()
    analysis_asset_id = 0
    status = False
    try:
        logger.info(f"LinkedIn profile analysis start. {profile_id=}")
        profile_json = profile_tool.filter_hirable_profile_data(profile_data)
        profile_text = json.dumps(profile_json)
        # analyze using OpenAI
        html = await analyzer.analyze_linkedin_profile(profile_text, job_types)
        profile = await profile_service.get_profile_details(profile_id)
        download_url = await file.handle_upload_pdf(
            html,
            profile["user_hash"],
            prefix="linkedin-profile-analysis",
        )
        analysis_asset_id = await asset_service.insert_asset(profile["user_id"], download_url, "ANALYSIS")
        await profile_service.upsert_analysis(profile_id, analysis_asset_id, JobAnalysisStatus.SUCCESS, profile["wp_user_id"])
        status = bool(analysis_asset_id)
    except OpenAIError as error:
        logger.error(f"Profile analysis failed during OpenAI client request. {error}")
        await profile_service.upsert_analysis(
            profile_id, None, JobAnalysisStatus.FAILED_NON_RETRYABLE, profile.get("wp_user_id")
        )
    except Exception as error:
        logger.error(f"Profile analysis failed during internal processes. {error}")
        await profile_service.upsert_analysis(
            profile_id, None, JobAnalysisStatus.FAILED_RETRYABLE, profile.get("wp_user_id")
        )
    finally:
        elapsed = dt.datetime.now(dt.UTC).timestamp() - start_time
        logger.info(f"LinkedIn profile analysis finished. status: {status}. elapsed: {elapsed:.2f}s.")
