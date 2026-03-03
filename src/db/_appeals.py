from typing import Any, Dict, List, Optional

from utils.decorators import ensure_connected


class AppealsMixin:
    @ensure_connected
    async def is_in_process(self, appeal_id: int) -> bool:
        result = await self._connection.fetchrow(
            "SELECT in_process FROM appeals WHERE id = $1",
            appeal_id,
        )
        return bool(result["in_process"]) if result else False

    @ensure_connected
    async def set_in_process(self, appeal_id: int, in_process: bool) -> None:
        await self._connection.execute(
            "UPDATE appeals SET in_process = $1 WHERE id = $2",
            bool(in_process),
            appeal_id,
        )

    @ensure_connected
    async def set_reject_reason(self, appeal_id: int, reject_reason: str) -> None:
        await self._connection.execute(
            "UPDATE appeals SET reject_reason = $1 WHERE id = $2",
            reject_reason,
            appeal_id,
        )

    @ensure_connected
    async def is_rejected(self, appeal_id: int) -> bool:
        result = await self._connection.fetchrow(
            "SELECT is_rejected FROM appeals WHERE id = $1",
            appeal_id,
        )
        return bool(result["is_rejected"]) if result else False

    @ensure_connected
    async def get_user_id_by_appeal(self, appeal_id: int) -> int:
        result = await self._connection.fetchrow(
            "SELECT user_id FROM appeals WHERE id = $1",
            appeal_id,
        )
        return int(result["user_id"]) if result else 0

    @ensure_connected
    async def create_appeal(
        self,
        tg_id: int,
        category: str,
        message: str,
        photo_id: str,
        geo_text: str = None,
        latitude: float = None,
        longitude: float = None,
    ) -> None:
        await self._connection.execute(
            """
            INSERT INTO appeals (
                user_id,
                category,
                message,
                reject_reason,
                photo_id,
                geo_text,
                latitude,
                longitude
            )
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            """,
            tg_id,
            category,
            message,
            "",
            photo_id,
            geo_text,
            latitude,
            longitude,
        )

    @ensure_connected
    async def get_appeal_by_id(
        self,
        appeal_id: int,
    ) -> Optional[Dict[str, Any]]:
        result = await self._connection.fetchrow(
            "SELECT * FROM appeals WHERE id = $1",
            appeal_id,
        )
        return dict(result) if result else None

    @ensure_connected
    async def get_user_appeals(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            "SELECT * FROM appeals WHERE user_id = $1 ORDER BY created_at DESC LIMIT $2 OFFSET $3",
            user_id,
            limit,
            offset,
        )
        return [dict(row) for row in rows]

    @ensure_connected
    async def get_unmoderated_appeals(
        self,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            """
            SELECT *
            FROM appeals
            WHERE is_accepted = FALSE and is_rejected = FALSE
            ORDER BY created_at ASC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        return [dict(row) for row in rows]

    @ensure_connected
    async def get_moderated_appeals(
        self,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            """
            SELECT *
            FROM appeals
            WHERE is_accepted = TRUE
            ORDER BY created_at ASC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        return [dict(row) for row in rows]

    @ensure_connected
    async def get_rejected_appeals(
        self,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            """
            SELECT *
            FROM appeals
            WHERE is_rejected = TRUE
            ORDER BY created_at ASC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        return [dict(row) for row in rows]

    @ensure_connected
    async def accept_appeal(self, appeal_id: int) -> None:
        await self._connection.execute(
            "UPDATE appeals SET is_accepted = TRUE WHERE id = $1",
            appeal_id,
        )

    @ensure_connected
    async def reject_appeal(self, appeal_id: int) -> None:
        await self._connection.execute(
            "UPDATE appeals SET is_rejected = TRUE WHERE id = $1",
            appeal_id,
        )

    @ensure_connected
    async def delete_appeal(self, appeal_id: int) -> None:
        await self._connection.execute(
            "DELETE FROM appeals WHERE id = $1",
            appeal_id,
        )

    @ensure_connected
    async def get_user_appeals_count(self, user_id: int) -> int:
        result = await self._connection.fetchrow(
            "SELECT COUNT(*) AS total FROM appeals WHERE user_id = $1",
            user_id,
        )
        return int(result["total"]) if result else 0

    @ensure_connected
    async def get_appeals_count(
        self, is_accepted: Optional[bool] = None, is_rejected: Optional[bool] = None
    ) -> int:
        if is_accepted is None and is_rejected is None:
            result = await self._connection.fetchrow(
                "SELECT COUNT(*) AS total FROM appeals",
            )
        else:
            result = await self._connection.fetchrow(
                "SELECT COUNT(*) AS total FROM appeals WHERE is_accepted = $1 and is_rejected = $2",
                bool(is_accepted),
                bool(is_rejected),
            )

        return int(result["total"]) if result else 0
