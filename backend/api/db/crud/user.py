"""Functions for crud operations with user table."""


from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.api.db.models import User


async def select_user_by_key(
    session: AsyncSession, key: str, show_detail_info: bool = False,
) -> Optional[User]:
    """
    Select user object by key.

    Args:
        session: Current database session.
        key: API key for obtaining user from database.
        show_detail_info: Show or not show detailed info.

    Returns:
        User obtained from database by key, or None if not found
    """
    if show_detail_info:
        query = (
            await session.execute(
                select(User).where(User.key == key).options(
                    joinedload(User.followers),
                    joinedload(User.following),
                ),
            )
        ).unique().scalar_one_or_none()

    else:
        query = (
            await session.execute(select(User).where(
                User.key == key,
                ),
            )
        ).unique().scalar_one_or_none()
    return query


async def select_user_by_id(
    session: AsyncSession, user_id: int, show_detail_info: bool = False,
) -> Optional[User]:
    """
    Select user object by ID.

    Args:
        session: Current database session.
        user_id: ID for obtaining user from database
        show_detail_info: Show or not show detailed info.

    Returns:
        User obtained from database by ID, or None if not found
    """
    if show_detail_info:
        query = (
            await session.execute(
                select(User).where(
                    User.id == user_id,
                ).options(
                    joinedload(User.followers),
                    joinedload(User.following),
                ),
            )
        ).unique().scalar_one_or_none()
    else:
        query = (
            await session.execute(select(User).where(User.id == user_id))
        ).unique().scalar_one_or_none()
    return query


async def add_user(
    user_key: str, user_name: str, session: AsyncSession,
) -> User:
    """
    Add user to the database.

    Args:
        user_key: API key of user.
        user_name: Username.
        session: Current database session.

    Returns:
        New user object.
    """
    new_user = User(key=user_key, name=user_name)
    session.add(new_user)
    await session.flush()
    return new_user
