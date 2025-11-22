import os
from dotenv import load_dotenv
from pathlib import Path

# load test environment variables
env_path = Path(__file__).resolve().parents[2] / "envs" / "app-test.env"
load_dotenv(env_path)
log_path = os.environ.get("LOG_PATH", "./logs/test-{}.log").format("application")
Path(log_path).parent.mkdir(parents=True, exist_ok=True)
db_url = os.environ.get("TEST_DATABASE_URL", "sqlite:///./tests/test.db")
if db_url.startswith("sqlite:///"):
    db_path = Path(db_url.replace("sqlite:///", ""))
    db_path.parent.mkdir(parents=True, exist_ok=True)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.tools.sql import Base
from app.schema.models import *
from main import app
from tests import mock


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine(os.environ["TEST_DATABASE_URL"])
    with engine.connect() as conn:
        conn.begin()
        conn.begin_nested()
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        session_generator = sessionmaker(bind=engine, autocommit=False)

        session = session_generator()

        @event.listens_for(session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction:
                conn.begin_nested()

        session.execute(text("PRAGMA foreign_keys=ON;"))

        yield session
        session.close()
        conn.rollback()


@pytest.fixture(autouse=True)
def clear_all_mocks(session: Session):
    yield
    mock.remove_all_mocks(session)
