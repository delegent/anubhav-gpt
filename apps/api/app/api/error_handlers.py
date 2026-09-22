from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.db.repositories import NotFoundError
from app.graph.nodes import ProviderError


def add_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError):
        return _error(request, 422, "VALIDATION_ERROR", "The request could not be validated.", list(exc.errors()))

    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        return _error(request, 404, "NOT_FOUND", str(exc), [])

    @app.exception_handler(ProviderError)
    async def provider_handler(request: Request, exc: ProviderError):
        return _error(request, exc.status_code, exc.code, str(exc), [])

    @app.exception_handler(Exception)
    async def unexpected_handler(request: Request, exc: Exception):
        return _error(request, 500, "INTERNAL_ERROR", "An unexpected error occurred.", [])


def _error(request: Request, status_code: int, code: str, message: str, details: list[object]):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": getattr(request.state, "request_id", "unknown"),
                "details": details,
            }
        },
    )
