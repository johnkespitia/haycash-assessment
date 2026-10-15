class CustomerNotFoundError(Exception):
    """Raised when a customer does not exist."""


class DuplicateCustomerEmailError(Exception):
    """Raised when a customer email is already registered."""