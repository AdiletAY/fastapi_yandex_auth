from typing import Dict

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from app.models.user import User
from app.utils.exc import DatabaseOperationError, DuplicateEntryError
from app.utils.logger import logger


class UserRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, instance: User) -> User:

        self._session.add(instance)

        try:
            await self._session.commit()
            await self._session.refresh(instance)
            return instance

        except IntegrityError as e:
            await self._handle_integrity_error(e)

        except SQLAlchemyError as e:
            await self._handle_sqlalchemy_error(e)

    async def get_one(self, **filters) -> User | None:
        statement = select(User)
        statement = await self._add_filters(statement, filters)

        try:
            result = await self._session.execute(statement)
            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            await self._handle_sqlalchemy_error(e)

    async def _add_filters(
        self,
        statement: Select,
        filter_conditions: Dict,
    ) -> Select:
        """
        Add filter conditions to a query statement.

        """
        if filter_conditions:
            statement = statement.filter_by(**filter_conditions)
        return statement

    async def _handle_integrity_error(self, e: IntegrityError):
        await self._session.rollback()
        logger.error("IntegrityError occurred: %s", str(e), exc_info=True)
        raise DuplicateEntryError(
            f"Duplicate entry detected. Details: {e.orig.args[0]}."
        ) from e

    async def _handle_sqlalchemy_error(self, e: SQLAlchemyError):
        await self._session.rollback()
        logger.error("SQLAlchemyError occurred: %s", str(e), exc_info=True)
        raise DatabaseOperationError(
            "An error occurred during the database operation. Details: %s", e
        ) from e
