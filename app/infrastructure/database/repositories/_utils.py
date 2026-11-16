from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


async def flush_and_commit(session: AsyncSession) -> None:
    try:
        await session.flush()
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise


def validate_pagination(limit: int, offset: int) -> None:
    if limit < 1:
        raise ValueError("limit must be greater than zero.")
    if offset < 0:
        raise ValueError("offset cannot be negative.")
