
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.application.ports.customer_repository import CustomerRepository
from app.domain.entities.customer import Customer
from app.domain.enums.customer_status import CustomerStatus
from app.domain.exceptions import DuplicateCustomerEmailError
from app.infrastructure.persistence.models.customer_model import CustomerModel
from app.infrastructure.persistence.repositories.base_repository import (
    BaseRepository,
)


class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repository = BaseRepository(session, CustomerModel)

    @staticmethod
    def _to_domain(model: CustomerModel) -> Customer:
        return Customer(
            id=model.id,
            name=model.name,
            email=model.email,
            status=CustomerStatus(model.status),
            created_at=model.created_at,
        )

    def create(self, customer: Customer) -> Customer:
        model = CustomerModel(
            id=customer.id,
            name=customer.name,
            email=customer.email,
            status=customer.status.value,
            created_at=customer.created_at,
        )

        try:
            self._repository.add(model)
            self._session.commit()
            self._session.refresh(model)
        except IntegrityError as exc:
            self._session.rollback()

            if getattr(exc.orig, "sqlstate", None) == "23505":
                raise DuplicateCustomerEmailError(
                    f"Customer with email '{customer.email}' already exists"
                ) from exc

            raise

        return self._to_domain(model)

    def get_by_id(self, customer_id: UUID) -> Customer | None:
        model = self._repository.get_by_id(customer_id)
        return self._to_domain(model) if model is not None else None

    def get_by_email(self, email: str) -> Customer | None:
        statement = select(CustomerModel).where(
            CustomerModel.email == email.strip().lower()
        )
        model = self._session.scalar(statement)

        return self._to_domain(model) if model is not None else None

    def list(
        self,
        status: CustomerStatus | None = None,
    ) -> list[Customer]:
        statement = select(CustomerModel).order_by(
            CustomerModel.created_at.desc()
        )

        if status is not None:
            statement = statement.where(
                CustomerModel.status == status.value
            )

        models = self._session.scalars(statement).all()
        return [self._to_domain(model) for model in models]

    def update(self, customer: Customer) -> Customer:
        model = self._repository.get_by_id(customer.id)

        if model is None:
            raise LookupError(f"Customer '{customer.id}' does not exist")

        model.name = customer.name
        model.email = customer.email
        model.status = customer.status.value

        self._repository.update(model)
        self._session.commit()
        self._session.refresh(model)

        return self._to_domain(model)
