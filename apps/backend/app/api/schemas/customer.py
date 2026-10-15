from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.domain.enums.customer_status import CustomerStatus


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr


class CustomerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    status: CustomerStatus
    created_at: datetime

class CustomerStatusUpdate(BaseModel):
    status: CustomerStatus