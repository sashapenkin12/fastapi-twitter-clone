"""
A module contains routes for media requests.

Attributes:
    router: FastAPI API router.
"""


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.app_service.schemas.responses import Response, UserResponse
from backend.api.app_service.service_functions import (generate_random_string,
                                                       get_api_key)
from backend.api.core.base import get_session
from backend.api.db.crud.user import (add_user, select_user_by_id,
                                      select_user_by_key)

router = APIRouter()


@router.post('/api/users/{user_id}/follow', response_model=Response)
async def follow_user(
        user_id: int,
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(get_session),
):
    """
    Follow a user.

    Args:
        user_id: ID of the user to follow.
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Result with a boolean value

    Raises:
        HTTPException: If the user is not found or is already followed.r

    """
    async with session.begin():
        curr_user = await select_user_by_key(session, api_key)
        if not curr_user:
            curr_user = await add_user(
                api_key,
                generate_random_string(),
                session,
            )

        user_to_follow = await select_user_by_id(
            session,
            user_id,
            show_detail_info=True,
        )
        if not user_to_follow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User to follow not found',
            )

        if curr_user in user_to_follow.followers:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='Already following this user',
            )

        user_to_follow.followers.append(curr_user)
        session.add(user_to_follow)

    return Response(result=True)


@router.delete('/api/users/{user_id}/follow', response_model=Response)
async def unfollow_user(
        user_id: int,
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(get_session),
):
    """
    Unfollow a user.

    Args:
        user_id: ID of the user to unfollow.
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Result with a boolean value.

    Raises:
        HTTPException: If the user you want to stop following
        has not been found or is not yet subscribed.
    """
    async with session.begin():
        curr_user = await select_user_by_key(session, api_key)
        if not curr_user:
            curr_user = await add_user(
                api_key,
                generate_random_string(),
                session,
            )

        user_to_unfollow = await select_user_by_id(
            session,
            user_id,
            show_detail_info=True,
        )
        if not user_to_unfollow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User to unfollow not found.',
            )

        if curr_user not in user_to_unfollow.followers:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail='Not following this user.',
            )

        user_to_unfollow.followers.remove(curr_user)
        session.add(user_to_unfollow)

    return Response(result=True)


@router.get('/api/users/me', response_model=UserResponse)
async def get_info_about_current_user(
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(get_session),
):
    """
    Get information about the current user.

    Args:
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Result with a boolean value and user information.
    """
    async with session.begin():
        curr_user = await select_user_by_key(session, api_key)
        if not curr_user:
            await add_user(
                api_key,
                generate_random_string(),
                session,
            )
        user = await select_user_by_key(
            session,
            api_key,
            show_detail_info=True,
        )
        user_dict = await user.to_dict()

        return UserResponse(result=True, user=user_dict)


@router.get('/api/users/{user_id}', response_model=UserResponse)
async def get_info_about_user(
        user_id: int,
        api_key: str = Depends(get_api_key),
        session: AsyncSession = Depends(get_session),
):
    """
    Get information about a user by ID.

    Args:
        user_id: ID of the user to retrieve.
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Result with a boolean value and user information.

    Raises:
        HTTPException: If required user is not found.
    """
    async with session.begin():
        curr_user = await select_user_by_key(session, api_key)
        if not curr_user:
            await add_user(
                api_key,
                generate_random_string(),
                session,
            )

        user = await select_user_by_id(
            session,
            user_id,
            show_detail_info=True,
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found',
            )

        user_dict = await user.to_dict()
        return UserResponse(result=True, user=user_dict)
