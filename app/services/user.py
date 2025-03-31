from uuid import UUID

from fastapi import HTTPException, status

from app.models.user import User
from app.repos.user import UserRepo
from app.schemas.user import UserCreate
from app.utils.exc import DatabaseOperationError, DuplicateEntryError


class UserService:
    def __init__(self, repo: UserRepo):
        self._repo = repo

    async def create(self, data: UserCreate) -> User:
        instance = User(**data.model_dump())

        try:
            user = await self._repo.create(instance)
            print(user)
            return user

        except DuplicateEntryError as e:
            self._handle_duplicate_entry_error(e)

        except DatabaseOperationError as e:
            self._handle_database_operation_error(e)

    async def get_by_id(self, id: UUID) -> User | None:
        try:
            return await self._repo.get_one(id=id)

        except DatabaseOperationError as e:
            self._handle_database_operation_error(e)

    async def get_by_yandex_id(self, yandex_id: str) -> User | None:
        try:
            return await self._repo.get_one(yandex_id=yandex_id)

        except DatabaseOperationError as e:
            self._handle_database_operation_error(e)

    @staticmethod
    def _handle_database_operation_error(e: DatabaseOperationError) -> None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    @staticmethod
    def _handle_duplicate_entry_error(e: DuplicateEntryError) -> None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
