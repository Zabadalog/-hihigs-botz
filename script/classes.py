"""Business logic class for Yandex Disk integration."""

from __future__ import annotations

import yadisk
import aiosqlite

from .db import DB_PATH

class YandexBotLogic:
    """Encapsulates interaction with Yandex Disk API and token storage."""

    def __init__(self, token: str | None = None) -> None:
        self._token = token
        self._client = yadisk.AsyncClient(token=token) if token else None

    def __repr__(self) -> str:  # magic method
        return f"YandexBotLogic(token_set={self._token is not None})"

    @property
    def token(self) -> str | None:
        return self._token

    async def save_token(self, user_id: int, token: str) -> None:
        """Save token for user and update client."""
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "INSERT OR REPLACE INTO yadisk_users(user_id, token) VALUES (?, ?)",
                (user_id, token),
            )
            await db.commit()
        self._token = token
        self._client = yadisk.AsyncClient(token=token)

    async def get_token(self, user_id: int) -> str | None:
        """Retrieve token from DB."""
        async with aiosqlite.connect(DB_PATH) as db:
            async with db.execute(
                "SELECT token FROM yadisk_users WHERE user_id=?", (user_id,)
            ) as cur:
                row = await cur.fetchone()
                return row[0] if row else None

    async def check_token(self) -> bool:
        """Check whether the stored token is valid."""
        if not self._client:
            return False
        try:
            return await self._client.check_token()
        except yadisk.exceptions.UnauthorizedError:
            return False

    async def add_folder(self, path: str) -> bool:
        """Try to create a folder on Yandex Disk."""
        if not self._client:
            return False
        try:
            if not await self._client.is_dir(path):
                await self._client.mkdir(path)
            return True
        except yadisk.YaDiskError:
            return False
