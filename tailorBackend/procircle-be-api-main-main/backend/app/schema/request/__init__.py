from pydantic import BaseModel


class BasePaginationSpec(BaseModel):
    page: int
    row: int
