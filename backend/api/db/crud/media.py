"""Functions for crud operations with media table."""


from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.models import Media, User


async def get_attachments_links_by_ids(
    session: AsyncSession, attachments_ids: List[int],
) -> List[str]:
    """
    Get links to images by their ID.

    Args:
        session: Current database session.
        attachments_ids: List of IDs of attachments that are needed.

    Returns:
        List of attachments links.
    """
    attachments_links = await session.execute(
        select(Media.link).where(
            Media.id.in_(attachments_ids),
        ),
    )
    return [row[0] for row in attachments_links.fetchall()]


async def add_media(
    file_name: Optional[str],
    user: User,
    scheme: str,
    host: str,
    session: AsyncSession,
) -> int:
    """
    Add images to the database.

    Args:
        file_name: File name.
        user: File uploader.
        scheme: Server HTTP scheme.
        host: Host of server.
        session: Current database session.

    Returns:
        ID of the new media.
    """
    new_media = Media(
        file_name=file_name,
        uploader=user,
        link='{0}://{1}/api/images/{2}'.format(
            scheme,
            host,
            file_name,
        ),
    )
    session.add(new_media)
    await session.flush()
    return new_media.id
