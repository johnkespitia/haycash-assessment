import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.api.dependencies import get_customer_service
from app.infrastructure.persistence.database import get_db_session
from app.main import app


@pytest.fixture(scope="session")
def test_engine():
    database_url = os.environ.get("TEST_DATABASE_URL")

    if not database_url:
        pytest.skip("TEST_DATABASE_URL is not configured")

    if database_url == os.environ.get("DATABASE_URL"):
        pytest.fail("Test database must be different from the development database")

    engine = create_engine(database_url, pool_pre_ping=True)

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def db_session(test_engine) -> Generator[Session, None, None]:
    connection = test_engine.connect()
    transaction = connection.begin()
    test_session_factory = sessionmaker(
        bind=connection,
        class_=Session,
        expire_on_commit=False,
    )
    session = test_session_factory()

    try:
        yield session
    finally:
        session.close()
        if transaction.is_active:
            transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_db_session():
        yield db_session

    def override_customer_service():
        from app.application.services.customer_service import CustomerService
        from app.infrastructure.persistence.repositories.sqlalchemy_customer_repository import (
            SqlAlchemyCustomerRepository,
        )

        repository = SqlAlchemyCustomerRepository(db_session)
        yield CustomerService(repository)

    app.dependency_overrides[get_db_session] = override_db_session
    app.dependency_overrides[get_customer_service] = override_customer_service

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
