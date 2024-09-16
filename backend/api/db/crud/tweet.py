"""Functions for crud operations with tweet table."""


from typing import List, Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.api.db.models import Tweet, User


async def select_tweet_by_id(
    session: AsyncSession, tweet_id: int,
) -> Optional[Tweet]:
    """
    Select tweet object by ID.

    Args:
        session: Current database session.
        tweet_id: ID for obtaining tweet from database.

    Returns:
        Tweet obtained from database by ID, or None if not found.
    """
    return (
        await session.execute(select(Tweet).where(
            Tweet.id == tweet_id,
            ),
        )
    ).unique().scalar_one_or_none()


async def select_all_tweets(session: AsyncSession) -> Sequence[Tweet]:
    """
    Select all tweet objects in the database.

    Args:
        session: Current database session.

    Returns:
        List of tweets obtained from database.
    """
    return (
        await session.execute(
            select(Tweet).order_by(Tweet.id).options(
                joinedload(Tweet.author),
            ),
        )
    ).unique().scalars().all()


async def add_tweet(
    tweet_data: str, attachments: List[int], user: User, session: AsyncSession,
) -> int:
    """
    Add a tweet to the database.

    Args:
        tweet_data: Tweet text data.
        attachments: List of links to the tweet's attachments.
        user: The author of the tweet.
        session: Current database session.

    Returns:
        ID of the new tweet.
    """
    new_tweet = Tweet(
        content=tweet_data,
        attachments=attachments,
        author=user,
    )
    session.add(new_tweet)
    await session.flush()
    return new_tweet.id
