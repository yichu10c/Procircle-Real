from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session


def test_guest_login(client: TestClient, session: Session):
    response = client.post(
        url="/v1/users/guest/login",
    )

    json_response = response.json()
    assert response.status_code == 200
    assert set(json_response.keys()) == {"data", "status", "message"}
