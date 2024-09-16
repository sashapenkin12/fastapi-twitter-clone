"""
A module contains routes for media requests.

Attributes:
    router: FastAPI API router.
"""


import os
from pathlib import Path

from aiofiles import open as async_open
from fastapi import APIRouter, Depends, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.app_service.schemas.responses import (AddMediaResponse,
                                                       ErrorResponse)
from backend.api.app_service.service_functions import (generate_random_string,
                                                       get_api_key)
from backend.api.core.base import get_session
from backend.api.db.crud.media import add_media
from backend.api.db.crud.user import add_user, select_user_by_key

router: APIRouter = APIRouter()


@router.get('/api/images/{file_name}')
async def get_image(file_name: str) -> FileResponse:
    """
    Get image by name.

    Args:
        file_name: Name of the file.

    Returns:
        FileResponse with the image file or an error message

    Raises:
        FileNotFoundError: If file doesn't exist on server.
    """
    file_path = Path(os.path.abspath('./backend/api/images/{0}'.format(
        file_name,
    )))
    if file_path.exists():
        return FileResponse(file_path)
    raise FileNotFoundError('File {0} not Found'.format(file_name))


@router.post('/api/medias', response_model=AddMediaResponse | ErrorResponse)
async def load_media(
    request: Request,
    file: UploadFile,
    api_key: str = Depends(get_api_key),
    session: AsyncSession = Depends(get_session),
):
    """
    Upload images to the server and add information about them to the database.

    Args:
        request: Current request argument.
        file: File to add.
        api_key: API key of the current user.
        session: Current database session.

    Returns:
        Dictionary with result and added media ID or error information
    """
    file_path = Path(
        os.path.abspath('./backend/api/images/{0}'.format(
            file.filename,
        ),
        ),
    )
    file_path.parent.mkdir(parents=True, exist_ok=True)

    async with async_open(file_path, mode='wb+') as local_file:
        content = await file.read()
        await local_file.write(content)

    async with session.begin():
        curr_user = await select_user_by_key(session, api_key)
        if not curr_user:
            await add_user(api_key, generate_random_string(), session)
        media_id = await add_media(
            file.filename,
            curr_user,
            request.url.scheme,
            request.client.host,
            session,
        )

    return {'result': True, 'media_id': media_id}
