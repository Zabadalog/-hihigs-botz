"""Async helpers for database creation."""

import aiosqlite

DB_PATH = "instance/sqlite.db"

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS yadisk_users (
    user_id INTEGER PRIMARY KEY,
    token TEXT
);
"""

async def create_table() -> None:
    """Create tables required for yadisk integration."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(CREATE_TABLE_QUERY)
        await db.commit()
