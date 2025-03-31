from app.schemas.base import BaseSchema


class UserCreate(BaseSchema):
    yandex_id: str
    email: str
    first_name: str
    last_name: str
