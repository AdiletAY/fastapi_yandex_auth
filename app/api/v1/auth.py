from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response

from app.api.deps.user import get_current_user, get_user_service
from app.models.user import User
from app.services.user import UserService
from app.utils.jwt_token import encode_jwt_token
from app.utils.yandex import (
    get_yandex_access_token_from_code,
    get_yandex_authorization_url,
    get_yandex_user_info,
)

router = APIRouter(prefix="/auth")


@router.get("/protected-api")
async def protected_api(user: Annotated[User, Depends(get_current_user)]):
    """Just for testing"""
    return user


@router.get("/yandex")
async def login_with_yandex():
    yandex_auth_url = await get_yandex_authorization_url()
    return {"auth_url": yandex_auth_url}


@router.get("/yandex/login/callback")
async def yandex_callback(
    code: Annotated[str, Query(...)],
    service: Annotated[UserService, Depends(get_user_service)],
):
    if not code:
        raise HTTPException(
            status_code=400,
            detail="No authorization code provided",
        )

    yandex_access_token = await get_yandex_access_token_from_code(code)

    user_data = await get_yandex_user_info(yandex_access_token)

    user = await service.get_by_yandex_id(yandex_id=user_data.yandex_id)

    if not user:
        user = await service.create(user_data)

    jwt_token = encode_jwt_token(str(user.id))

    response = Response(status_code=200)
    response.set_cookie(
        key="authToken",
        value=jwt_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=60 * 60,
    )
    return response
