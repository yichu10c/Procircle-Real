from fastapi import APIRouter, Depends, HTTPException, Request, Security
from sqlalchemy.ext.asyncio import AsyncSession
import os, httpx
from dotenv import load_dotenv

from app.controllers.v1 import li_profile_controller
from app.schema.request.li_profile_request import AnalyzeLinkedInProfileSpec
from app.schema.response.li_profile_response import (
    AnalyzeLinkedInProfileResponse,
    GetLinkedInProfileAnalysisResponse,
)
from app.tools.sql import connection
from app.tools.security.wp_token import verify_wp_token, wp_token_header

router = APIRouter(
    prefix="/profiles",
)

load_dotenv()
HCAPTCHA_SECRET = os.getenv("HCAPTCHA_SECRET")
APP_ENV = os.getenv("environment", "prod").lower()


async def verify_hcaptcha(token: str):
    if APP_ENV in {"local", "dev"}:
        return
    if not HCAPTCHA_SECRET:
        raise HTTPException(status_code=500, detail="hCaptcha secret not configured")
    async with httpx.AsyncClient() as client:
        resp = await client.post("https://hcaptcha.com/siteverify", data={
            "secret": HCAPTCHA_SECRET,
            "response": token,
        })
        result = resp.json()
        print("DEBUG hCaptcha verification result:", result)
        if not result.get("success", False):
            raise HTTPException(status_code=403, detail="hCaptcha verification failed")


@router.post("/analyze")
async def analyze_profile(
    spec: AnalyzeLinkedInProfileSpec,
    request: Request,
    token: str = Security(wp_token_header),
    session: AsyncSession = Depends(connection.get_session),
) -> AnalyzeLinkedInProfileResponse:
    # Verify captcha
    await verify_hcaptcha(spec.hcaptcha_token)

    # Verify WordPress token after captcha
    current_user_id = await verify_wp_token(request, token)

    # Always use the verified WordPress user id; ignore any client-supplied value
    spec.wp_user_id = current_user_id

    # Combine the fields into profile_data for the controller
    spec.profile_data = {
        "email": spec.email,
        "headline": spec.headline,
        "current_position": spec.current_position,
        "about": spec.about,
        "education": spec.education,
        "experience": spec.experience,
        "skills": spec.skills,
        "licenses_certifications": spec.licenses_certifications,
    }

    result = await li_profile_controller.analyze_profile(
        session, spec.profile_data, spec.job_types, current_user_id
    )
    return AnalyzeLinkedInProfileResponse(data=result)


@router.get("/analyze/result")
async def get_analysis_result(
    profile_id: int,
    wp_user_id: int | None = None,
    current_user_id: int = Depends(verify_wp_token),
    session: AsyncSession = Depends(connection.get_session),
) -> GetLinkedInProfileAnalysisResponse:
    result = await li_profile_controller.get_profile_analysis(
        session, profile_id, current_user_id
    )
    if not result:
        raise HTTPException(status_code=404, detail="analysis not found")
    return GetLinkedInProfileAnalysisResponse(data=result)
