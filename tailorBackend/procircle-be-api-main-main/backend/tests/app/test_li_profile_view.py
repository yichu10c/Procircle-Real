from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session
import base64
import hmac
import hashlib
import os
import time

from tests import mock
from app.views.v1 import li_profile_view


def _make_token(user_id: int) -> str:
    secret = os.environ["WP_SHARED_SECRET"]
    ts = int(time.time())
    sig = hmac.new(secret.encode(), f"{user_id}{ts}".encode(), hashlib.sha256).hexdigest()
    raw = f"{user_id}:{ts}:{sig}".encode()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()


def test_analyze_profile(client: TestClient, session: Session, monkeypatch):
    async def fake_verify(token: str):
        return None

    monkeypatch.setattr(li_profile_view, "verify_hcaptcha", fake_verify)

    from job_worker.task import analyze_task

    def fake_delay(profile_id: int, profile_data: dict, job_types: str):
        pass

    monkeypatch.setattr(analyze_task.start_linkedin_profile_analysis, "delay", fake_delay)

    token = _make_token(1)
    response = client.post(
        url="/v1/profiles/analyze",
        headers={"X-WP-Token": token},
        json={
            "email": "test@example.com",
            "headline": "Tester",
            "job_types": "software",
            "hcaptcha_token": "token",
            # Provide a mismatched wp_user_id; it should be overwritten by the token
            "wp_user_id": 999,
        },
    )
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}

    from app.schema.models.li_profile_model import LinkedInProfile

    profile = session.get(LinkedInProfile, json_response["data"]["profile_id"])
    assert profile.wp_user_id == 1


def test_get_profile_analysis_result(client: TestClient, session: Session):
    user = mock.create_dummy_user(session)
    profile = mock.create_dummy_profile(session, user.id)
    asset = mock.create_dummy_analysis_result(session, user.id)
    mock.create_dummy_profile_analysis(session, profile.id, asset.id)
    token = _make_token(1)
    # Send a mismatched wp_user_id query parameter; it should be ignored
    response = client.get(
        url="/v1/profiles/analyze/result",
        headers={"X-WP-Token": token},
        params={"profile_id": profile.id, "wp_user_id": 999},
    )
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}


def test_profile_analysis_without_temp_dir(
    client: TestClient, session: Session, monkeypatch
):
    """Ensure PDF generation works when `.temp` does not exist."""
    import os
    import shutil
    import asyncio

    from job_worker.controller import analyze_controller
    from job_worker.task import analyze_task
    from job_worker.tools import analyzer
    from tools.aws import s3
    import pdfkit

    # remove temp folder if present
    if os.path.exists(".temp"):
        shutil.rmtree(".temp")

    # mocks
    async def fake_analyze_linkedin_profile(profile_text: str, job_types: str) -> str:
        return "<html><body>ok</body></html>"

    def fake_pdf_from_string(content: str, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(b"pdf")

    upload_args = {}

    def fake_upload_file(filepath: str, key: str) -> str:
        upload_args["path"] = filepath
        upload_args["key"] = key
        return f"https://example.com/{key}"

    task_params = {}

    def fake_delay(profile_id: int, profile_data: dict, job_types: str):
        task_params.update({
            "profile_id": profile_id,
            "profile_data": profile_data,
            "job_types": job_types,
        })

    from app.services import asset_service, profile_service
    from app.repository import li_profile_query

    async def fake_insert_asset(user_id: int, url: str, asset_type: str) -> int:
        return 1

    async def fake_upsert_analysis(
        profile_id: int,
        result_asset_id: int,
        status: int,
        wp_user_id: int,
    ) -> int:
        return 1

    async def fake_get_profile_details(profile_id: int) -> dict:
        return {"user_id": user.id, "user_hash": user.hash, "wp_user_id": 1}

    monkeypatch.setattr(
        analyzer, "analyze_linkedin_profile", fake_analyze_linkedin_profile
    )
    monkeypatch.setattr(pdfkit, "from_string", fake_pdf_from_string)
    monkeypatch.setattr(s3, "upload_file", fake_upload_file)

    async def fake_insert_profile(
        sess, user_id: int, profile_data: str, job_types: str, wp_user_id: int
    ) -> int:
        return 1

    monkeypatch.setattr(analyze_task.start_linkedin_profile_analysis, "delay", fake_delay)
    monkeypatch.setattr(li_profile_query, "insert_profile", fake_insert_profile)
    monkeypatch.setattr(asset_service, "insert_asset", fake_insert_asset)
    monkeypatch.setattr(profile_service, "upsert_analysis", fake_upsert_analysis)
    monkeypatch.setattr(profile_service, "get_profile_details", fake_get_profile_details)

    user = mock.create_dummy_user(session)

    async def fake_verify(token: str):
        return None

    monkeypatch.setattr(li_profile_view, "verify_hcaptcha", fake_verify)

    token = _make_token(1)
    response = client.post(
        url="/v1/profiles/analyze",
        headers={"X-WP-Token": token},
        json={
            "email": "a@b.com",
            "job_types": "software",
            "hcaptcha_token": "token",
            "wp_user_id": 1,
        },
    )

    # execute the patched analysis synchronously
    asyncio.run(
        analyze_controller.handle_linkedin_profile_analysis(
            task_params["profile_id"],
            task_params["profile_data"],
            task_params["job_types"],
        )
    )

    assert response.status_code == 200
    assert upload_args.get("path", "").startswith(".temp/")
    assert not os.path.exists(upload_args["path"])
