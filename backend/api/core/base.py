"""
A module contains class for database session control and get_session coroutine.

Attributes:
    Base: Declarative base.
    sessionmanager: An instance of DatabaseSessionManager class.
"""


from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator

from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.pool import NullPool

from backend.api.db.db_service import check_tables

Base: DeclarativeBase = declarative_base()


class DatabaseSessionManager:
    """
    Database connection session manager.

    Attributes:
        _engine: SQLAlchemy engine.
        _sessionmaker: Async database sessionmaker.
    """

    def __init__(self):
        """Initialize the database engine and sessionmaker with None values."""
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        """
        Initialize the database engine and sessionmaker with the provided host.

        Args:
            host: Database connection string.
        """
        self._engine = create_async_engine(host, poolclass=NullPool)
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            bind=self._engine,
        )

    async def startup(self):
        """Start manager: Initializes metadata if necessary."""
        async with self.connect() as conn:
            if not await self.check_tables_exists(conn):
                await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def drop_all(cls, connection: AsyncConnection):
        """
        Drop all tables and relationships in database.

        Args:
            connection: An active database connection.
        """
        await connection.run_sync(Base.metadata.drop_all)

    @classmethod
    async def create_all(cls, connection: AsyncConnection):
        """
        Create all tables and relationships in database.

        Args:
            connection: An active database connection.
        """
        await connection.run_sync(Base.metadata.create_all)

    async def close(self):
        """
        Shutdown manager.

        if it has not been initialized, an exception is thrown.

        Raises:
            RuntimeError: If DatabaseSessionManager is not initialized.
        """
        if self._engine is None:
            raise RuntimeError('DatabaseSessionManager is not initialized.')
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Connect to the database.

        Yields:
            An active database connection.

        Raises:
            RuntimeError: If DatabaseSessionManager is not initialized.
            Exception: If any exception occurred during the connection yield.

        """
        if self._engine is None:
            raise RuntimeError('DatabaseSessionManager is not initialized.')

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Initialize a session.

        Yields:
            AsyncSession: An active database session.

        Raises:
            RuntimeError: If the DatabaseSessionManager is not initialized.
            Exception: If any other exception occurs during the session yield.

        """
        if self._sessionmaker is None:
            raise RuntimeError('DatabaseSessionManager is not initialized.')

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    @classmethod
    async def check_tables_exists(cls, connection: AsyncConnection) -> bool:
        """
        Check for table existence: used when starting the manager.

        Args:
            connection: Async connection to database.

        Returns:
            If tables exists return True else False.
        """
        return await connection.run_sync(
            lambda sync_conn: check_tables(sync_conn),
        )

    @property
    def engine(self) -> AsyncEngine:
        """
        Get SQLAlchemy engine.

        Returns:
            SQLAlchemy async engine.
        """
        return self._engine


sessionmanager = DatabaseSessionManager()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get session generator.

    Yields:
        An active database session.
    """
    async with sessionmanager.session() as session:
        yield session
