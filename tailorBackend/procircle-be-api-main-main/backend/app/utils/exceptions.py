"""
Exception File
"""
from logging import Logger
from typing import Any, Dict, Optional

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError

from app.schema.response import BaseResponseSchema, ResponseStatusEnum
from tools.observability.log import get_logger


class ApplicationException(Exception):
    def __init__(
        self,
        message: str = "",
        data: Optional[Dict[Any, Any]] = None,
        status_code: int = 500,
        status: ResponseStatusEnum = ResponseStatusEnum.FAILED,
        error: Exception = None
    ):
        self.message = message
        self.data = data
        self.status = status
        self.status_code = status_code
        self.error = error

        if not message:
            self.message = str(error) if error else ""

    @property
    def response(self):
        return JSONResponse(
            BaseResponseSchema(
                data=self.data,
                status=self.status,
                message=self.message,
            ).model_dump(),
            self.status_code
        )


async def application_error_handler(request: Request, error: ApplicationException):
    """
    ApplicationException and Exception handler

    Any exception will be caught and returned with the specified return format
    """
    logger: Logger = await get_logger(request)
    logger.error(
        f"ApplicationException exception captured. data={error.data}. message='{error.message}'. "
        f"status_code={error.status_code}. status={error.status.value}."
    )
    return error.response


async def validation_error_handler(request: Request, error: RequestValidationError | ResponseValidationError):
    """
    ApplicationException and Exception handler

    Any exception will be caught and returned with the specified return format
    """
    logger: Logger = await get_logger(request)
    logger.error(f"Request/Response validation error captured. errors={error.errors()}")
    result = BaseResponseSchema(data=error.errors(), status=ResponseStatusEnum.CONTRACT_VIOLATION)
    return JSONResponse(result.model_dump(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def exception_handler(request: Request, error: Exception):
    """
    ApplicationException and Exception handler

    Any exception will be caught and returned with the specified return format
    # """
    if isinstance(error, ApplicationException):
        return await application_error_handler(request, error)
    if isinstance(error, (RequestValidationError, ResponseValidationError)):
        return await validation_error_handler(request, error)
    logger: Logger = await get_logger(request)
    logger.error(f"Uncaught exception captured {error}", error)
    result = BaseResponseSchema(data=None, status=ResponseStatusEnum.FAILED, message=str(error))
    return JSONResponse(result.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
