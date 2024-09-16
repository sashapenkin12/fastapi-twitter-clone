"""
A module contains exception handlers.

This module contains the following handlers:
    exception_handler: A handler that returns a False result value
     and error information.
"""


from typing import Dict

from fastapi import Request
from fastapi.responses import JSONResponse, Response


async def exception_handler(request: Request, exc: Exception) -> Response:
    """
    Return a False result value and error information.

    Args:
        request: Current request of client.
        exc: Occurred error.

    Returns:
        Response with a False result value and error information.
    """
    response: Dict[str, bool | str] = {
        'result': False,
        'error_type': type(exc).__name__,
        'error_message': str(exc),
    }
    return JSONResponse(response)
