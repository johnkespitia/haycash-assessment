from enum import StrEnum


class CustomerStatus(StrEnum):
	ACTIVE = "ACTIVE"
	PENDING = "PENDING"
	BLOCKED = "BLOCKED"
