from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    CustomerNotFoundError,
    DuplicateCustomerEmailError,
)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DuplicateCustomerEmailError)
    async def duplicate_email_handler(
        request: Request,
        exc: DuplicateCustomerEmailError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.exception_handler(CustomerNotFoundError)
    async def customer_not_found_handler(
        request: Request,
        exc: CustomerNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )
