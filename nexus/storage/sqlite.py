from __future__ import annotations

import sqlite3

from .base import StorageProvider


class SQLiteStorage(StorageProvider):

    def __init__(
        self,
        database: str = "data/nexus.db",
    ):

        self.connection = sqlite3.connect(
            database
        )

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS storage(
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )

    def save(
        self,
        key: str,
        value,
    ):

        self.connection.execute(
            """
            INSERT OR REPLACE
            INTO storage(key,value)
            VALUES(?,?)
            """,
            (
                key,
                value,
            ),
        )

        self.connection.commit()

    def load(
        self,
        key: str,
    ):

        row = self.connection.execute(
            "SELECT value FROM storage WHERE key=?",
            (key,),
        ).fetchone()

        if row:
            return row[0]

        return None

    def delete(
        self,
        key: str,
    ):

        self.connection.execute(
            "DELETE FROM storage WHERE key=?",
            (key,),
        )

        self.connection.commit()

    def exists(
        self,
        key: str,
    ):

        return self.load(key) is not None

    def keys(self):

        rows = self.connection.execute(
            "SELECT key FROM storage"
        ).fetchall()

        return [
            row[0]
            for row in rows
        ]
