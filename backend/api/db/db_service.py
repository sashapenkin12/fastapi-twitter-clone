"""A module contains application function for db service."""


from sqlalchemy import inspect


def check_tables(sync_conn) -> bool:
    """
    Check the existence of tables in a database.

    Args:
        sync_conn: Synchronous connection with the database.

    Returns:
        True if tables exist, otherwise False.
    """
    inspector = inspect(sync_conn)
    tables = inspector.get_table_names()
    return bool(tables)
