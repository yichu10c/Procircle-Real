"""
User View
"""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.v1 import user_controller
from app.tools.sql import connection
from app.schema.request.user_request import ExtendSessionSpec
from app.schema.response.user_response import ExtendSessionResponse, GuestLoginResponse


router = APIRouter(prefix="/users")


@router.post("/guest/login")
async def guest_login(
    request: Request,
    session: AsyncSession = Depends(connection.get_session)
) -> GuestLoginResponse:
    """
    Guest login
    """
    token = await user_controller.guest_login(request, session)
    return GuestLoginResponse(data=token)


@router.post("/guest/extend_session")
async def extend(
    request: Request,
    spec: ExtendSessionSpec
) -> ExtendSessionResponse:
    """
    Extend guest session
    """
    token = await user_controller.guest_extend_session(request, spec.token)
    return ExtendSessionResponse(data=token)
