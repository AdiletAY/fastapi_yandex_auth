"""

It is just a simplified version I would rather write a class
or use the lib: https://github.com/LulzLoL231/YandexID

"""

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.schemas.yandex import YandexUserSchema


async def get_yandex_authorization_url():
    yandex_auth_url = (
        f"https://oauth.yandex.ru/authorize?response_type=code"
        f"&client_id={settings.oauth.yandex.client_id}&redirect_uri={settings.oauth.yandex.redirect_uri}"
    )
    return yandex_auth_url


async def get_yandex_access_token_from_code(code: str) -> str:
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth.yandex.ru/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "client_id": settings.oauth.yandex.client_id,
                "client_secret": settings.oauth.yandex.client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.oauth.yandex.redirect_uri,
            },
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to obtain access token")

        token_data = token_response.json()
        access_token = token_data.get("access_token")

    return access_token


async def get_yandex_user_info(access_token: str) -> YandexUserSchema:
    async with httpx.AsyncClient() as client:
        user_response = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch user info")

        user_data = user_response.json()

    return YandexUserSchema(
        yandex_id=user_data["id"],
        email=user_data["default_email"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
    )
