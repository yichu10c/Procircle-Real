"""
User Response
"""
from app.schema.response import BaseResponseSchema

class GuestLoginResponse(BaseResponseSchema):
    data: str

class ExtendSessionResponse(BaseResponseSchema):
    data: str
