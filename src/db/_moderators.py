from typing import Any, Dict, List, Optional

from utils.decorators import ensure_connected


class ModeratorsMixin:
    @ensure_connected
    async def is_moderator(self, tg_id: int) -> bool:
        return await self._connection.fetchval(
            "SELECT EXISTS(SELECT 1 FROM moderators WHERE tg_id = $1)",
            tg_id,
        )
        
    @ensure_connected
    async def make_moderator(self, tg_id: int) -> None:
        await self._connection.execute(
            "INSERT INTO moderators (tg_id) VALUES ($1) ON CONFLICT (tg_id) DO NOTHING",
            tg_id,
        )
        
    @ensure_connected
    async def remove_moderator(self, tg_id: int) -> None:
        await self._connection.execute(
            "DELETE FROM moderators WHERE tg_id = $1",
            tg_id,
        )
        
    @ensure_connected
    async def get_moderators(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            """
            SELECT
                moderators.*,
                users.username
            FROM moderators
            JOIN users USING (tg_id)
            ORDER BY moderators.created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset
        )
        return [dict(row) for row in rows]
    
    @ensure_connected
    async def get_moderators_count(self) -> int:
        return await self._connection.fetchval(
            "SELECT COUNT(*) FROM moderators"
        )
        
    @ensure_connected
    async def get_moderator_data(self, tg_id: int) -> Optional[Dict[str, Any]]:
        row = await self._connection.fetchrow(
            """
            SELECT
                moderators.*,
                users.username,
                users.is_banned
            FROM moderators
            JOIN users USING (tg_id)
            WHERE tg_id = $1
            """,
            tg_id
        )
        return dict(row) if row else None
    
    @ensure_connected
    async def add_rejected_count(self, tg_id: int, add: int) -> None:
        await self._connection.execute(
            """
            UPDATE
                moderators
            SET rejected_appeals = rejected_appeals + $1
            WHERE tg_id = $2
            """,
            abs(add),
            tg_id
        )
        
    @ensure_connected
    async def add_accepted_count(self, tg_id: int, add: int) -> None:
        await self._connection.execute(
            """
            UPDATE
                moderators
            SET accepted_appeals = accepted_appeals + $1
            WHERE tg_id = $2
            """,
            abs(add),
            tg_id
        )
        
