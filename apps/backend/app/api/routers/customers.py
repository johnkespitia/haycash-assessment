from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.dependencies import CustomerServiceDependency
from app.api.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerStatusUpdate,
)
from app.domain.enums.customer_status import CustomerStatus

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    payload: CustomerCreate,
    service: CustomerServiceDependency,
) -> CustomerResponse:
    customer = service.create_customer(
        name=payload.name,
        email=str(payload.email),
    )

    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        email=customer.email,
        status=customer.status,
        created_at=customer.created_at,
    )

@router.get("", response_model=list[CustomerResponse])
def list_customers(
    service: CustomerServiceDependency,
    customer_status: Annotated[
        CustomerStatus | None,
        Query(alias="status"),
    ] = None
) -> list[CustomerResponse]:
    return service.list_customers(status=customer_status)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: UUID,
    service: CustomerServiceDependency,
) -> CustomerResponse:
    return service.get_customer(customer_id)


@router.patch(
    "/{customer_id}/status",
    response_model=CustomerResponse,
)
def update_customer_status(
    customer_id: UUID,
    payload: CustomerStatusUpdate,
    service: CustomerServiceDependency,
) -> CustomerResponse:
    return service.update_customer_status(
        customer_id=customer_id,
        status=payload.status,
    )
