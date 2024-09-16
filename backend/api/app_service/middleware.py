"""
A module contains middleware for requests logging.

Attributes:
    logger (Logger): A logger with an error level required to
     display current information about the operation of functions.
"""


import logging
import time

from fastapi import Request, Response
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger('uvicorn.error')


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware required for logging requests data."""

    @classmethod
    async def dispatch(cls, request: Request, call_next) -> Response:
        """
        Show info about current request.

        Args:
            request: Current client request.
            call_next: Function that routes the request.

        Returns:
            Response of the request.

        """
        logger.info('Headers: {0}'.format(request.headers))
        request_body = await request.body()
        logger.info('Body: {0}'.format(request_body))
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response_body = [chunk async for chunk in response.body_iterator]
        logger.info('Process time: {0}'.format(process_time))
        try:
            logger.info('Response: {0}'.format(response_body[0].decode()))
        except UnicodeDecodeError:
            logger.info(
                'Failed to decode in utf-8. Hex response: {0}'.format(
                    response_body[0],
                ),
            )
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        return response
