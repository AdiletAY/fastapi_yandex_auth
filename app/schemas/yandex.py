from pydantic import BaseModel


class YandexUserSchema(BaseModel):
    yandex_id: str
    email: str
    first_name: str
    last_name: str
