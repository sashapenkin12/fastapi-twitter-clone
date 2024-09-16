"""
A module contains routes for tweet requests.

Attributes:
    router: FastAPI API router.
"""


from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.app_service.schemas.models import InputTweet
from backend.api.app_service.schemas.responses import (AddTweetResponse,
                                                       Response,
                                                       TweetsResponse)
from backend.api.app_service.service_functions import (generate_random_string,
                                                       get_api_key)
from backend.api.core.base import get_session
from backend.api.db.crud.media import get_attachments_links_by_ids
from backend.api.db.crud.tweet import (add_tweet, select_all_tweets,
                                       select_tweet_by_id)
from backend.api.db.crud.user import add_user, select_user_by_key

router: APIRouter = APIRouter()


@router.post('/api/tweets', response_model=AddTweetResponse)
async def create_tweet(
    tweet: InputTweet,
    api_key: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
):
    """
    Add a tweet to the database.

    Args:
        tweet: Tweet to add.
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Result with a boolean value and added tweet ID.
    """
    tweet_media_ids: Optional[List[int]] = tweet.tweet_media_ids

    async with session.begin():
        curr_user = await select_user_by_key(session, api_key)
        if not curr_user:
            curr_user = await add_user(
                api_key,
                generate_random_string(),
                session,
            )

        attachments = []
        if tweet_media_ids:
            attachments = await get_attachments_links_by_ids(
                session,
                tweet_media_ids,
            )

        tweet_id = await add_tweet(
            tweet.tweet_data,
            attachments,
            curr_user,
            session,
        )

    return AddTweetResponse(result=True, tweet_id=tweet_id)


@router.delete('/api/tweets/{tweet_id}', response_model=Response)
async def delete_tweet(
    tweet_id: int,
    api_key: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
):
    """
    Delete a tweet.

    Args:
        tweet_id: ID of the tweet to delete.
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Result with a boolean value

    Raises:
        HTTPException: If tweet not found or user can't delete this tweet.
    """
    async with session.begin():
        curr_user = await select_user_by_key(session, api_key)
        if not curr_user:
            curr_user = await add_user(
                api_key,
                generate_random_string(),
                session,
            )

        tweet = await select_tweet_by_id(session, tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tweet not found',
            )

        if curr_user.id != tweet.author_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not authorized to delete this tweet',
            )

        await session.delete(tweet)

    return Response(result=True)


@router.post(
    '/api/tweets/{tweet_id}/likes',
    response_model=Response,
)
async def like_tweet(
    tweet_id: int,
    api_key: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
):
    """
    Add a like to a tweet.

    Args:
        tweet_id: ID of the tweet to like.
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Result with a boolean value

    Raises:
        HTTPException: If tweet not found or already liked.
    """
    async with session.begin():
        curr_user = await select_user_by_key(session, api_key)
        if not curr_user:
            curr_user = await add_user(
                api_key,
                generate_random_string(),
                session,
            )

        tweet = await select_tweet_by_id(session, tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tweet not found.',
            )

        if curr_user in tweet.likes:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='Tweet already liked.',
            )

        tweet.likes.append(curr_user)
        session.add(tweet)
    return Response(result=True)


@router.delete('/api/tweets/{tweet_id}/likes', response_model=Response)
async def unlike_tweet(
    tweet_id: int,
    api_key: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
):
    """
    Remove a like from a tweet.

    Args:
        tweet_id: ID of the tweet to unlike.
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Result with a boolean value

    Raises:
        HTTPException: If tweet not found or was not liked.
    """
    async with session.begin():
        curr_user = await select_user_by_key(session, api_key)
        if not curr_user:
            curr_user = await add_user(
                api_key,
                generate_random_string(),
                session,
            )

        tweet = await select_tweet_by_id(session, tweet_id)
        if not tweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Tweet not found.',
            )

        if curr_user not in tweet.likes:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='Tweet was not liked.',
            )
        tweet.likes.remove(curr_user)
        session.add(tweet)
    return Response(result=True)


@router.get('/api/tweets', response_model=TweetsResponse)
async def get_all_tweets(
    api_key: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
):
    """
    Get the tweet feed.

    Args:
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Result with a boolean value and a list of tweets.
    """
    curr_user = await select_user_by_key(session, api_key)
    if not curr_user:
        await add_user(api_key, generate_random_string(), session)

    tweets = await select_all_tweets(session)
    tweets = [await tweet.to_dict() for tweet in tweets]

    return TweetsResponse(result=True, tweets=tweets)
