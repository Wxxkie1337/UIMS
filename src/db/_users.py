from typing import Any, Dict, List, Optional

from utils.decorators import ensure_connected
from config import OWNERS_ID


class UsersMixin:
    @ensure_connected
    async def add_user(self, tg_id: int, username: str) -> None:
        await self._connection.execute(
            "INSERT INTO users (tg_id, username) VALUES ($1, $2) ON CONFLICT (tg_id) DO NOTHING",
            tg_id, username
        )

    @ensure_connected
    async def is_banned(self, tg_id: int) -> bool:
        result = await self._connection.fetchrow(
            "SELECT is_banned FROM users WHERE tg_id = $1",
            tg_id,
        )
        return bool(result["is_banned"]) if result else False

    @ensure_connected
    async def ban_user(self, tg_id: int) -> None:
        if tg_id in OWNERS_ID:
            return
        
        await self._connection.execute(
            "UPDATE users SET is_banned = TRUE WHERE tg_id = $1",
            tg_id,
        )

    @ensure_connected
    async def unban_user(self, tg_id: int) -> None:
        if tg_id in OWNERS_ID:
            return
        
        await self._connection.execute(
            "UPDATE users SET is_banned = FALSE WHERE tg_id = $1",
            tg_id,
        )
        
    @ensure_connected
    async def set_last_ui_id(self, tg_id: int, message_id: int) -> None:
        await self._connection.execute(
            "UPDATE users SET last_ui_message_id = $1 WHERE tg_id = $2",
            message_id, tg_id
        )

    @ensure_connected
    async def get_last_ui_id(self, tg_id: int) -> Optional[int]:
        return await self._connection.fetchval(
            "SELECT last_ui_message_id FROM users WHERE tg_id = $1",
            tg_id,
        )
        
    @ensure_connected
    async def get_banned_users(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            """
            SELECT *
            FROM users
            WHERE is_banned
            ORDER BY tg_id DESC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset
        )
        return [dict(row) for row in rows]
    
    @ensure_connected
    async def get_banned_users_count(self) -> int:
        return await self._connection.fetchval(
            "SELECT COUNT(*) FROM users WHERE is_banned"
        )
        
    @ensure_connected
    async def get_user_data(self, tg_id: int) -> Optional[Dict[str, Any]]:
        row = await self._connection.fetchrow(
            """
            SELECT
                *
            FROM users
            WHERE tg_id = $1
            """,
            tg_id
        )
        return dict(row) if row else None