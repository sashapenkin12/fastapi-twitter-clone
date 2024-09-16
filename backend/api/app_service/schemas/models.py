"""A module contains schemas for database data validation."""

from typing import List, Optional

from pydantic import BaseModel


class BaseModelWithConfig(BaseModel):
    """Basic schema model with settings."""

    class Config:
        """Nested class for configuration of basemodel."""

        model_config = {'from_attributes': True}


class BasicUserSchema(BaseModelWithConfig):
    """
    Schema for displaying user information.

    Attributes:
        user_id: User ID.
        name: Username.

    """

    user_id: int
    name: str


class AlternativeUserSchema(BaseModelWithConfig):
    """
    An alternative schema for displaying user information.

    Attributes:
        id: User ID.
        name: Username.

    """

    id: int
    name: str


class UserSchema(AlternativeUserSchema):
    """
    Detailed version of the schema for displaying information about the user.

    Attributes:
        followers: List of user's subscribers.
        following: List of users the user is subscribed to.

    """

    followers: List[AlternativeUserSchema] = []
    following: List[AlternativeUserSchema] = []


class TweetSchema(BaseModelWithConfig):
    """
    Schema for displaying information about a tweet.

    Attributes:
        id: Tweet ID.
        content: Text content of the tweet.
        attachments: List of links to the tweet's attachments.
        author: The author of the tweet.
        likes: List of users who liked a tweet.

    """

    id: int
    content: str
    attachments: List[str] = []
    author: AlternativeUserSchema
    likes: List[BasicUserSchema] = []


class InputTweet(BaseModelWithConfig):
    """
    Schema for validating the body of a tweet add request.

    Attributes:
        tweet_data: Text content of the tweet.
        tweet_media_ids: List of tweet IDs.

    """

    tweet_data: str
    tweet_media_ids: Optional[List[int]]
