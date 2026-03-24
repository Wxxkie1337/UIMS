from typing import Any, Dict, List, Optional

from utils.decorators import ensure_connected


class AdminMixin:
    @ensure_connected
    async def is_admin(self, tg_id: int) -> bool:
        return await self._connection.fetchval(
            "SELECT EXISTS(SELECT 1 FROM admins WHERE tg_id = $1)",
            tg_id,
        )
    
    @ensure_connected
    async def make_admin(self, tg_id: int) -> None:
        await self._connection.execute(
            "INSERT INTO admins (tg_id) VALUES ($1) ON CONFLICT (tg_id) DO NOTHING",
            tg_id,
        )
        
    @ensure_connected
    async def remove_admin(self, tg_id: int) -> None:
        await self._connection.execute(
            "DELETE FROM admins WHERE tg_id = $1",
            tg_id,
        )
        
    @ensure_connected
    async def get_admins(self, offset: int, limit: int) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            """
            SELECT
                admins.*,
                users.username
            FROM admins
            JOIN users USING (tg_id)
            ORDER BY admins.created_at DESC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset
        )
        return [dict(row) for row in rows]
    
    @ensure_connected
    async def get_admins_count(self) -> int:
        return await self._connection.fetchval(
            "SELECT COUNT(*) FROM admins"
        )
        
    @ensure_connected
    async def get_admin_data(self, tg_id: int) -> Optional[Dict[str, Any]]:
        row = await self._connection.fetchrow(
            """
            SELECT
                admins.*,
                users.username,
                users.is_banned
            FROM admins
            JOIN users USING (tg_id)
            WHERE admins.tg_id = $1
            """,
            tg_id
        )
        return dict(row) if row else None