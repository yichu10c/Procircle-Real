"""
User Query
"""
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.models.user_model import GuestUser
from app.tools.sql.query_wrapper import within, as_dict


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> Dict[str, Any]:
    """
    """
    user = await (
        within(session)
        .select(GuestUser)
        .where(GuestUser.id == user_id)
        .first()
    )
    return as_dict(user)


async def get_user_by_hash(
    session: AsyncSession,
    user_hash: str,
) -> Dict[str, Any]:
    """
    """
    return await (
        within(session)
        .select(GuestUser)
        .where(GuestUser.hash == user_hash)
        .first()
    )


async def insert_user(
    session: AsyncSession,
    user_hash: str,
):
    """
    """
    return await (
        within(session)
        .insert(GuestUser)
        .values({GuestUser.hash: user_hash})
        .insert_row()
    )
