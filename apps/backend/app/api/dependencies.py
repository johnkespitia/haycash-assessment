from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.services.customer_service import CustomerService
from app.infrastructure.persistence.database import get_db_session
from app.infrastructure.persistence.repositories.sqlalchemy_customer_repository import (
    SqlAlchemyCustomerRepository,
)


def get_customer_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> CustomerService:
    repository = SqlAlchemyCustomerRepository(session)
    return CustomerService(repository)


CustomerServiceDependency = Annotated[
    CustomerService,
    Depends(get_customer_service),
]
