from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from app.schema.models.job_model import Job, JobMatch, JobMatchAnalysis
from app.tools.resource import file
from app.utils.exceptions import ApplicationException
from tests import mock


def test_get_job_list(client: TestClient, session: Session):
    # prepare
    job = mock.create_dummy_job(session)

    # act
    response = client.get(
        url="/v1/jobs",
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}
    assert len(json_response["data"]) == 1
    assert json_response["data"][0]["job_title"] == job.job_title


def test_get_job_details_success(client: TestClient, session: Session):
    # prepare
    job = mock.create_dummy_job(session)

    # act
    response = client.get(
        url=f"/v1/jobs/{job.id}",
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}
    assert json_response["data"]["job_title"] == job.job_title


def test_get_job_details_invalid_id(client: TestClient, session: Session):
    # act
    response = client.get(
        url="/v1/jobs/0",
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}
    assert json_response["data"] == None


def test_score_job_match_by_resume_id_and_job_id_success(
    client: TestClient,
    session: Session
):
    """
    """
    # prepare
    user = mock.create_dummy_user(session)
    job = mock.create_dummy_job(session)
    resume = mock.create_dummy_resume(session, user.id)

    # act
    response = client.post(
        url="/v1/jobs/match",
        headers={
            "Authorization": f"Bearer {user.token}"
        },
        json={
            "resume_id": resume.id,
            "job_id": job.id,
        }
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}
    assert "score" in json_response["data"].keys()


def test_score_job_match_by_resume_id_and_job_id_invalid(
    client: TestClient,
    session: Session
):
    """
    """
    # prepare
    user = mock.create_dummy_user(session)
    resume = mock.create_dummy_resume(session, user.id)

    # act
    try:
        response = client.post(
            url="/v1/jobs/match",
            headers={
                "Authorization": f"Bearer {user.token}"
            },
            json={
                "resume_id": resume.id,
                "job_id": 123,
            }
        )
    except Exception as e:
        assert isinstance(e, ApplicationException)


def test_score_job_match_by_resume_id_and_job_desc_text_success(
    client: TestClient,
    session: Session
):
    """
    """
    # prepare
    user = mock.create_dummy_user(session)
    resume = mock.create_dummy_resume(session, user.id)

    # act
    response = client.post(
        url="/v1/jobs/match",
        headers={
            "Authorization": f"Bearer {user.token}"
        },
        json={
            "resume_id": resume.id,
            "job_desc_text": "best job ever",
        }
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}
    assert "score" in json_response["data"].keys()


def test_score_job_match_by_resume_id_and_job_desc_id_success(
    client: TestClient,
    session: Session
):
    """
    """
    # prepare
    user = mock.create_dummy_user(session)
    job_desc = mock.create_dummy_job_desc(session, user.id)
    resume = mock.create_dummy_resume(session, user.id)

    # act
    response = client.post(
        url="/v1/jobs/match",
        headers={
            "Authorization": f"Bearer {user.token}"
        },
        json={
            "resume_id": resume.id,
            "job_desc_id": job_desc.id,
        }
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}
    assert "score" in json_response["data"].keys()


def test_job_match_history(
    client: TestClient,
    session: Session
):
    # prepare
    user = mock.create_dummy_user(session)
    job_desc = mock.create_dummy_job_desc(session, user.id)
    resume = mock.create_dummy_resume(session, user.id)
    job_match = mock.create_dummy_job_match(
        session, user.id, resume.id, None, job_desc.id
    )

    # act
    response = client.get(
        url="/v1/jobs/match/history",
        headers={
            "Authorization": f"Bearer {user.token}"
        }
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}
    assert len(json_response["data"]) == 1


def test_analyze_job_match_success(
    client: TestClient,
    session: Session
):
    """
    """
    # prepare
    user = mock.create_dummy_user(session)
    job_desc = mock.create_dummy_job_desc(session, user.id)
    resume = mock.create_dummy_resume(session, user.id)
    job_match = mock.create_dummy_job_match(
        session, user.id, resume.id, None, job_desc.id
    )

    # act
    response = client.post(
        url="/v1/jobs/analyze",
        headers={
            "Authorization": f"Bearer {user.token}"
        },
        json={
            "job_match_id": job_match.id
        }
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}


def test_analyze_job_match_success(
    client: TestClient,
    session: Session
):
    """
    """
    # prepare
    user = mock.create_dummy_user(session)
    job_desc = mock.create_dummy_job_desc(session, user.id)
    resume = mock.create_dummy_resume(session, user.id)
    job_match = mock.create_dummy_job_match(
        session, user.id, resume.id, None, job_desc.id
    )

    # act
    response = client.post(
        url="/jobs/analyze",
        headers={
            "Authorization": f"Bearer {user.token}"
        },
        json={
            "job_match_id": job_match.id
        }
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}


def test_get_job_match_result_success(
    client: TestClient,
    session: Session
):
    """
    """
    # prepare
    user = mock.create_dummy_user(session)
    job_desc = mock.create_dummy_job_desc(session, user.id)
    resume = mock.create_dummy_resume(session, user.id)
    job_match = mock.create_dummy_job_match(
        session, user.id, resume.id, None, job_desc.id
    )

    # act
    response = client.get(
        url="/v1/jobs/analyze/result",
        headers={
            "Authorization": f"Bearer {user.token}"
        },
        params={
            "job_match_id": job_match.id
        }
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}


def test_get_job_match_result_invalid(
    client: TestClient,
    session: Session
):
    """
    """
    # prepare
    user = mock.create_dummy_user(session)

    # act
    response = client.get(
        url="/jobs/analyze/result",
        headers={
            "Authorization": f"Bearer {user.token}"
        },
        params={
            "job_match_id": 0
        }
    )

    # assert
    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}
