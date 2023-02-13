"""
Database utility functions.

"""
import sqlite3
import logging

from sqlite3 import Connection
from typing import List, Dict, Any


class DatabaseContextManager:
    """
    Database Context Manager class for SQLite3 database connections.
    """

    def __init__(self, database_name: str) -> None:
        self.database_name = database_name

    def __enter__(self) -> Connection:
        self.connection = sqlite3.connect(self.database_name)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    # TODO: Implement logging capabilities
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.connection.close()

# TODO: Implement logging capabilities
class DatabaseConnection:
    """
    Class to encapsulate Sqlite3 database operations.
    """

    DATABASE_CONNECTION_COUNT = 0
    # Counts the number of database connections while the service is up.

    def __init__(self, database_name: str):
        self.database_name = database_name

    def count_database_connections(self) -> None:
        """
        Count the number of database connections.
        """
        self.DATABASE_CONNECTION_COUNT += 1
    # TODO: insert into database the number of database connections 
    def execute(self, *args, **kwargs) -> Any:
        with DatabaseContextManager(self.database_name) as connection:
            cursor = connection.cursor()
            cursor.execute(*args, **kwargs)
            connection.commit()
            self.count_database_connections()
            return cursor.fetchall()

    def get_post(self, post_id: int) -> Any:
        """
        Get a post from the database using its ID.
        """
        post = self.execute(
            f"SELECT * FROM posts WHERE id = {post_id}"
        )
        return post
