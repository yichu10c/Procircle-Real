"""
User Request Spec
"""
from pydantic import BaseModel


class ExtendSessionSpec(BaseModel):
    token: str
