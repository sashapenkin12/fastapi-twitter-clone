"""
A module containing functions for the application to operate.

This module contains these coroutines:
    startup: Required to start the database session manager.
    shutdown: Required to shut down the database session manager.
    get_api_key: Required to get api-key header of a request.
And these Functions:
    generate_random_string: Required to generate random username
     for authorization.

Attributes:
    logger (Logger): A logger with an error level required to
     display current information about the operation of functions.
"""


import logging
from secrets import choice
from string import ascii_lowercase

from fastapi import HTTPException, Request, status

from backend.api.core.base import sessionmanager

logger = logging.getLogger('uvicorn.error')


async def startup() -> None:
    """Start the session manager."""
    logger.info('Starting sessionmanager...')
    await sessionmanager.startup()
    logger.info('Sessionmanager started')


async def shutdown():
    """Close sessionmanager if needed."""
    if sessionmanager.engine is not None:
        logger.info('Closing sessionmanager...')
        await sessionmanager.close()
        logger.info('Sessionmanager closed')


async def get_api_key(request: Request) -> str:
    """
    Obtain the authorization key.

    Args:
        request: Current request of client.

    Returns:
        Api-key header of a request.

    Raises:
        HTTPException: If request header 'api-key' doesn't exist.
    """
    api_key = request.headers.get('api-key')
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='API key missing',
        )

    return api_key


def generate_random_string() -> str:
    """
    Generate a random username for authorization.

    Returns:
        Username for authorization.
    """
    username_length = 14
    return ''.join(choice(ascii_lowercase) for _ in range(username_length))
