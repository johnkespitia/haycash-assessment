from abc import ABC, abstractmethod
from collections.abc import Sequence
from uuid import UUID

from app.domain.entities.customer import Customer
from app.domain.enums.customer_status import CustomerStatus


class CustomerRepository(ABC):

    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        """Persist a new customer."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, customer_id: UUID) -> Customer | None:
        """Return a customer by ID, or None if it does not exist."""
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> Customer | None:
        """Return a customer by email, or None if it does not exist."""
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        status: CustomerStatus | None = None,
    ) -> Sequence[Customer]:
        """Return customers, optionally filtered by status."""
        raise NotImplementedError

    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        """Persist changes to an existing customer."""
        raise NotImplementedError