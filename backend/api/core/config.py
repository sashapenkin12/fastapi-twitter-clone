"""
A module with class for database engine config.

Attributes:
    config: An instance of Config class.
"""


import os


class Config:
    """
    Class for getting the current database configuration.

    (written in environment in docker-compose.yml)

    Attributes:
        db_config: Database config initialized in os environment.
    """

    db_config: str = os.getenv(
        'DB_CONFIG',
        'postgresql+asyncpg:' +
        '//{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'.format(
            DB_USER=os.getenv('DB_USER', 'fastapi'),
            DB_PASSWORD=os.getenv('DB_PASSWORD', 'fastapi-password'),
            DB_HOST=os.getenv('DB_HOST', 'fastapi-postgresql:5432'),
            DB_NAME=os.getenv('DB_NAME', 'fastapi'),
        ),
    )


config = Config
