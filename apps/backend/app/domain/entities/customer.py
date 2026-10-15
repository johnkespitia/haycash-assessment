from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.domain.enums.customer_status import CustomerStatus


@dataclass
class Customer:
	id: UUID
	name: str
	email: str
	status: CustomerStatus
	created_at: datetime
