"""
JWT Handler
"""
import os
import jwt
from typing import Any, Dict

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"

def encode(data: dict):
    assert isinstance(data, dict), "only dict type is allowed"
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def decode(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, [ALGORITHM])
