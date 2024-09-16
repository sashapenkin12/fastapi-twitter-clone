"""App module with app initialization function."""
from fastapi import FastAPI

from backend.api.app_service.exception_handlers import exception_handler
from backend.api.app_service.middleware import LoggingMiddleware
from backend.api.app_service.service_functions import shutdown, startup
from backend.api.core.base import sessionmanager
from backend.api.core.config import config
from backend.api.routes.media import router as media_router
from backend.api.routes.tweet import router as tweet_router
from backend.api.routes.user import router as user_router


def init_app(init_db=True) -> FastAPI:
    """
    Initialize the application.

    And if required, the database.

    Args:
        init_db (bool): Initialize the database or not.

    Returns:
        FastAPI app with routers.
    """
    if init_db:
        sessionmanager.init(config.db_config)

    server = FastAPI(title='FastAPI server')
    server.add_event_handler('startup', startup)
    server.add_event_handler('shutdown', shutdown)
    server.add_middleware(LoggingMiddleware)
    server.add_exception_handler(Exception, exception_handler)
    server.include_router(user_router)
    server.include_router(tweet_router)
    server.include_router(media_router)

    return server
