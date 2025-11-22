"""
Authorization and Authentication Handler
"""
import uuid
import datetime as dt
from typing import Any, Coroutine

from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from fastapi import status

from app.schema.response import ResponseStatusEnum
from app.tools.sql.connection import async_session
from app.repository import user_query
from app.tools.security import jwt
from app.utils.exceptions import ApplicationException


class APIAuth(HTTPBearer):
    def __init__(self):
        super().__init__()

    async def __call__(self, request: Request) -> Coroutine[Any, Any, HTTPAuthorizationCredentials | None]:
        try:
            credentials = await super().__call__(request)
            user = await self.validate_token(credentials.credentials)
            request.state.current_user = user
            return credentials
        except HTTPException as e:
            raise e
        except Exception as e:
            raise ApplicationException(
                message=str(e),
                status=ResponseStatusEnum.UNAUTHORIZED,
                status_code=status.HTTP_401_UNAUTHORIZED
            )

    async def validate_token(self, jwt_token: str):
        async with async_session() as session:
            # validate token
            credential = jwt.decode(jwt_token)
            if not validate_credentials(credential):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

            # validate token session
            if credential["expired_at"] < dt.datetime.now(dt.UTC).timestamp():
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="session expired")

            # validate guest user
            user = await user_query.get_user_by_hash(session, credential["user_hash"])
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

        return user


api_authentication = APIAuth()


def get_current_user(request: Request) -> user_query.GuestUser:
    """
    """
    try:
        return request.state.current_user
    except:
        pass


def generate_user_hash():
    """
    """
    return uuid.uuid4().hex


def generate_session_token(user_hash: str):
    """
    """
    return jwt.encode(
        {
            "user_hash": user_hash,
            "expired_at": (dt.datetime.now(dt.UTC) + dt.timedelta(hours=12)).timestamp()
        }
    )


def validate_credentials(token_or_cred: str | dict) -> bool:
    """
    """
    try:
        credential = token_or_cred if isinstance(token_or_cred, dict) else jwt.decode(token_or_cred)
        return len(set(credential.keys()) - {"user_hash", "expired_at"}) == 0
    except:
        return False


def get_user_hash_from_token(jwt_token: str):
    """
    """
    return jwt.decode(jwt_token)["user_hash"]


def generate_guest_token() -> str:
    user_hash = generate_user_hash()
    return generate_session_token(user_hash)
