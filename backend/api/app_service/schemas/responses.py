"""A module contains schemas for responses validation."""


from typing import List

from backend.api.app_service.schemas.models import (BaseModelWithConfig,
                                                    TweetSchema, UserSchema)


class Response(BaseModelWithConfig):
    """
    Schema for a basic answer.

    Attributes:
        result: A bool value indicating whether the result exists or not.

    """

    result: bool


class UserResponse(Response):
    """
    Schema for a response that returns the user.

    Attributes:
        user: User object.

    """

    user: UserSchema


class ErrorResponse(Response):
    """
    Schema for a response that returns an error.

    Attributes:
        error_type: The type of error that occurred.
        error_message: Message of error.

    """

    error_type: str
    error_message: str


class TweetsResponse(Response):
    """
    Schema for a response that returns a list of tweets.

    Attributes:
        tweets: List of tweet objects.
    """

    tweets: List[TweetSchema] = []


class AddMediaResponse(Response):
    """
    Response schema that returns the number of the image.

    Attributes:
        media_id: Media ID.
    """

    media_id: int


class AddTweetResponse(Response):
    """
    Schema for a response that returns the number of the tweet created.

    Attributes:
        tweet_id: Tweet ID.
    """

    tweet_id: int
