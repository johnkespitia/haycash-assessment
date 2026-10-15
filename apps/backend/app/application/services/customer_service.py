
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.application.ports.customer_repository import CustomerRepository
from app.domain.entities.customer import Customer
from app.domain.enums.customer_status import CustomerStatus
from app.domain.exceptions import (
    CustomerNotFoundError,
    DuplicateCustomerEmailError,
)


class CustomerService:
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    def create_customer(self, name: str, email: str) -> Customer:
        normalized_email = email.strip().lower()

        existing_customer = self._repository.get_by_email(normalized_email)
        if existing_customer is not None:
            raise DuplicateCustomerEmailError(
                f"Customer with email '{normalized_email}' already exists"
            )

        customer = Customer(
            id=uuid4(),
            name=name.strip(),
            email=normalized_email,
            status=CustomerStatus.PENDING,
            created_at=datetime.now(UTC),
        )

        return self._repository.create(customer)

    def get_customer(self, customer_id: UUID) -> Customer:
        customer = self._repository.get_by_id(customer_id)

        if customer is None:
            raise CustomerNotFoundError(
                f"Customer with ID '{customer_id}' was not found"
            )

        return customer

    def list_customers(
        self,
        status: CustomerStatus | None = None,
    ) -> list[Customer]:
        return list(self._repository.list(status=status))

    def update_customer_status(
        self,
        customer_id: UUID,
        status: CustomerStatus,
    ) -> Customer:
        customer = self.get_customer(customer_id)

        updated_customer = Customer(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            status=status,
            created_at=customer.created_at,
        )

        return self._repository.update(updated_customer)
