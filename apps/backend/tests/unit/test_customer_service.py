
from uuid import UUID

import pytest

from app.application.services.customer_service import CustomerService
from app.domain.enums.customer_status import CustomerStatus
from app.domain.exceptions import (
    CustomerNotFoundError,
    DuplicateCustomerEmailError,
)
from tests.unit.fakes.fake_customer_repository import FakeCustomerRepository


@pytest.fixture
def repository() -> FakeCustomerRepository:
    return FakeCustomerRepository()


@pytest.fixture
def service(repository: FakeCustomerRepository) -> CustomerService:
    return CustomerService(repository)


def test_create_customer_starts_as_pending(
    service: CustomerService,
) -> None:
    customer = service.create_customer(
        name="John Espitia",
        email="John@example.com",
    )

    assert isinstance(customer.id, UUID)
    assert customer.name == "John Espitia"
    assert customer.email == "john@example.com"
    assert customer.status == CustomerStatus.PENDING
    assert customer.created_at is not None


def test_create_customer_rejects_duplicate_email(
    service: CustomerService,
) -> None:
    service.create_customer("John", "john@example.com")

    with pytest.raises(DuplicateCustomerEmailError):
        service.create_customer("Another John", "JOHN@example.com")


def test_get_customer_returns_existing_customer(
    service: CustomerService,
) -> None:
    created = service.create_customer("John", "john@example.com")

    result = service.get_customer(created.id)

    assert result == created


def test_get_customer_raises_when_not_found(
    service: CustomerService,
) -> None:
    missing_id = UUID("00000000-0000-0000-0000-000000000001")

    with pytest.raises(CustomerNotFoundError):
        service.get_customer(missing_id)


def test_list_customers_filters_by_status(
    service: CustomerService,
    repository: FakeCustomerRepository,
) -> None:
    pending = service.create_customer("Pending", "pending@example.com")
    active = service.create_customer("Active", "active@example.com")

    repository.update(
        type(active)(
            id=active.id,
            name=active.name,
            email=active.email,
            status=CustomerStatus.ACTIVE,
            created_at=active.created_at,
        )
    )

    result = service.list_customers(status=CustomerStatus.ACTIVE)

    assert len(result) == 1
    assert result[0].id == active.id
    assert result[0].id != pending.id


def test_update_customer_status_preserves_other_fields(
    service: CustomerService,
) -> None:
    created = service.create_customer("John", "john@example.com")

    updated = service.update_customer_status(
        created.id,
        CustomerStatus.BLOCKED,
    )

    assert updated.status == CustomerStatus.BLOCKED
    assert updated.id == created.id
    assert updated.name == created.name
    assert updated.email == created.email
    assert updated.created_at == created.created_at
