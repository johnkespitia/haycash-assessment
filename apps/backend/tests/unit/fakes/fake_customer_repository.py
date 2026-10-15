
from uuid import UUID

from app.domain.entities.customer import Customer
from app.domain.enums.customer_status import CustomerStatus


class FakeCustomerRepository:
    def __init__(self) -> None:
        self._customers: dict[UUID, Customer] = {}

    def create(self, customer: Customer) -> Customer:
        if self.get_by_email(customer.email) is not None:
            raise ValueError("Email already exists")

        self._customers[customer.id] = customer
        return customer

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        return self._customers.get(customer_id)

    def get_by_email(self, email: str) -> Customer | None:
        normalized_email = email.strip().lower()

        return next(
            (
                customer
                for customer in self._customers.values()
                if customer.email == normalized_email
            ),
            None,
        )

    def list(
        self,
        status: CustomerStatus | None = None,
    ) -> list[Customer]:
        customers = list(self._customers.values())

        if status is not None:
            customers = [
                customer
                for customer in customers
                if customer.status == status
            ]

        return customers

    def update(self, customer: Customer) -> Customer:
        if customer.id not in self._customers:
            raise KeyError(f"Customer {customer.id} does not exist")

        self._customers[customer.id] = customer
        return customer
