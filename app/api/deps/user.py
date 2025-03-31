from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from jwt.exceptions import DecodeError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import database
from app.models.user import User
from app.repos.user import UserRepo
from app.services.user import UserService
from app.utils.jwt_token import decode_jwt_token

cookie_scheme = APIKeyCookie(name="authToken")


async def get_user_service(
    session: Annotated[AsyncSession, Depends(database.get_session)],
) -> UserService:
    repo = UserRepo(session)
    return UserService(repo)


async def get_current_user(
    token: Annotated[str, Depends(cookie_scheme)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:

    d_token = decode_jwt_token(token)

    user = await service.get_by_id(d_token.sub)

    if not user:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")

    return user
