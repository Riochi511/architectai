import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database import get_db
from app.auth.dependencies import get_current_user
from app.main import app

from app.models import (
    User,
    Project,
    Requirement,
    Architecture,
)


TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session():

    Base.metadata.create_all(
        bind=engine
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

        Base.metadata.drop_all(
            bind=engine
        )


@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    test_user = User(
        id=1,
        full_name="Test User",
        email="test@example.com",
        hashed_password="test-password",
        is_active=True,
    )

    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    def override_current_user():
        return test_user

    app.dependency_overrides[
        get_db
    ] = override_get_db

    app.dependency_overrides[
        get_current_user
    ] = override_current_user

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
