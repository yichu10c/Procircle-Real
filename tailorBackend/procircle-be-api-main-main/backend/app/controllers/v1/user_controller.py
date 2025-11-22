from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from tools.observability.log import get_logger
from app.tools.security import auth, jwt
from app.repository import user_query
from app.schema.data.user import UserToken
from app.schema.response import ResponseStatusEnum
from app.utils.exceptions import ApplicationException


async def guest_login(
    request: Request,
    session: AsyncSession,
) -> str:
    """
    """
    logger = await get_logger(request)

    try:
        # create user
        user_hash = auth.generate_user_hash()
        await user_query.insert_user(session, user_hash)

        # construct session token
        token = auth.generate_session_token(user_hash)
        return token

    except Exception as e:
        logger.error(f"failed to login due to {e}")
        raise e


async def guest_extend_session(
    request: Request,
    token: str
) -> str:
    """
    """
    logger = await get_logger(request)

    try:
        # validate credentials
        if not auth.validate_credentials(token):
            raise ApplicationException("invalid token", status_code=401)

        # re-construct session token
        user_hash = auth.get_user_hash_from_token(token)
        token = auth.generate_session_token(user_hash)
        return token

    except Exception as e:
        logger.error(f"failed to extend session due to {e}")
        raise e
