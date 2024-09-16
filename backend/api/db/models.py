"""
A module contains ORM models.

Attributes:
    followers_association: Table for followers/following relationship.
    likes_table: Table for likes relationship.
"""


from typing import List

from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, Relationship, relationship

from backend.api.core.base import Base

USER_ID_FIELD = 'users.id'
USER_MODEL_NAME = 'User'

MAX_NAME_LENGTH = 25
MAX_CONTENT_LENGTH = 500

followers_association: Table = Table(
    'followers',
    Base.metadata,
    Column(
        'follower_id',
        Integer,
        ForeignKey(USER_ID_FIELD),
    ),
    Column(
        'followed_id',
        Integer,
        ForeignKey(USER_ID_FIELD),
    ),
)

likes_table: Table = Table(
    'likes',
    Base.metadata,
    Column(
        'user_id',
        Integer,
        ForeignKey(USER_ID_FIELD),
    ),
    Column(
        'tweet_id',
        Integer,
        ForeignKey('tweets.id'),
    ),
)


class User(Base):
    """
    User model.

    Attributes:
        __tablename__: Table name.
        id: User ID column.
        key: User key column.
        name: Username column.
        followers: User followers relationship.
    """

    __tablename__: str = 'users'

    id: Mapped[Column[Integer]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    key: Mapped[Column[String]] = Column(String, nullable=False, unique=True)
    name: Mapped[Column[String]] = Column(
        String(MAX_NAME_LENGTH),
        nullable=False,
    )

    followers = relationship(
        USER_MODEL_NAME,
        secondary=followers_association,
        primaryjoin=id == followers_association.c.followed_id,
        secondaryjoin=id == followers_association.c.follower_id,
        backref='following',
        lazy='joined',
    )

    async def to_dict(self) -> dict:
        """
        Format a user object into a dictionary.

        Returns:
            User detail info in dict format.
        """
        followers: List[dict] = [
            await follower.alt_to_repr()
            for follower in self.followers
        ] if self.followers else []
        following: List[dict] = [
            await following.alt_to_repr()
            for following in self.following
        ] if self.following else []
        return {
            'id': self.id,
            'name': self.name,
            'followers': followers,
            'following': following,
        }

    async def to_repr(self) -> dict:
        """
        Format a user object into a dictionary for repr.

        Returns:
            User brief info.
        """
        return {'user_id': self.id, 'name': self.name}

    async def alt_to_repr(self) -> dict:
        """
        Alternative format a user object into a dictionary for repr.

        Returns:
            User brief info.
        """
        return {'id': self.id, 'name': self.name}


class Tweet(Base):
    """
    Tweet model.

    Attributes:
        __tablename__: Table name.
        id: Tweet ID column.
        content: Text content column.
        attachments: Array of tweet attachments links column.
        author_id: Author of the tweet ID.
        author: User table relationship; foreign key is author_id.
        likes: Users who liked relationship

    """

    __tablename__: str = 'tweets'

    id: Mapped[Column[Integer]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    content: Mapped[Column[String]] = Column(
        String(MAX_CONTENT_LENGTH),
        nullable=False,
    )
    attachments: Mapped[Column[ARRAY]] = Column(ARRAY(String))
    author_id: Mapped[Column[Integer]] = Column(
        Integer,
        ForeignKey(USER_ID_FIELD),
    )
    author: Mapped[Relationship] = relationship(
        USER_MODEL_NAME,
        foreign_keys=author_id,
        lazy='joined',
    )
    likes = relationship(
        USER_MODEL_NAME,
        secondary=likes_table,
        lazy='joined',
    )

    async def to_dict(self) -> dict:
        """
        Format a tweet object into a dictionary.

        Returns:
            Tweet detail info in dict format.
        """
        author: dict = await self.author.alt_to_repr() if self.author else None
        likes: List[dict] = [
            await like.to_repr()
            for like in self.likes
        ] if self.likes else []
        return {
            'id': self.id,
            'content': self.content,
            'attachments': self.attachments,
            'author': author,
            'likes': likes,
        }


class Media(Base):
    """
    Media model.

    Attributes:
        __tablename__: Table name.
        id: Media ID column.
        uploader_id: Media uploader ID column.
        uploader: User table relationship.
        file_name: File name.
        link: Link to media in backend.
    """

    __tablename__: str = 'media'

    id: Mapped[Column[Integer]] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    uploader_id: Mapped[Column[Integer]] = Column(
        Integer,
        ForeignKey('users.id'),
    )
    uploader: Mapped[Relationship] = relationship('User')
    file_name: Mapped[Column[String]] = Column(String, nullable=False)
    link: Mapped[Column[String]] = Column(String, nullable=False)
