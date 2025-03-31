from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
import msgspec

from app.core.config import settings


class Token(msgspec.Struct):
    sub: str


def _decode_payload(encoded_token: str):
    return jwt.decode(
        jwt=encoded_token,
        key=settings.jwt.secret_key,
        algorithms=[settings.jwt.algorithm],
    )


def decode_jwt_token(encoded_token: str):
    payload = _decode_payload(encoded_token=encoded_token)

    return msgspec.convert(payload, Token, strict=False)


def encode_jwt_token(user_id: str) -> str:
    return jwt.encode(
        payload={
            "sub": user_id,
            "exp": datetime.now(timezone.utc)
            + timedelta(minutes=settings.jwt.token_time),
        },
        key=settings.jwt.secret_key,
        algorithm=settings.jwt.algorithm,
    )
