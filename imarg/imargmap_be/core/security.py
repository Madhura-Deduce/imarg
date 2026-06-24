from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_HOURS
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(data: dict):

    payload = data.copy()

    payload["exp"] = (
        datetime.utcnow()
        + timedelta(
            hours=ACCESS_TOKEN_EXPIRE_HOURS
        )
    )

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )