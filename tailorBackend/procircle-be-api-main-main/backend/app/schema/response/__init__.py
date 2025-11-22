import enum
from typing import Any, Optional
from pydantic import BaseModel, field_serializer


class ResponseStatusEnum(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CONTRACT_VIOLATION = "CONTRACT VIOLATIONS"
    UNAUTHORIZED = "UNAUTHORIZED"


class BaseResponseSchema(BaseModel):
    data: Optional[Any] = None
    status: ResponseStatusEnum = ResponseStatusEnum.SUCCESS
    message: str = ""

    @field_serializer("status")
    def serialize_status(status: ResponseStatusEnum):
        return status.value

