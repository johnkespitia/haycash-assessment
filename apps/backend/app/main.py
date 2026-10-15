
from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.routers.customers import router as customers_router

app = FastAPI(
    title="Customer API",
    description="Customer management API for the Haycash assessment",
    version="1.0.0",
)

register_exception_handlers(app)
app.include_router(customers_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
