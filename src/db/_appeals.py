from typing import Any, Dict, List, Optional

from utils.decorators import ensure_connected


class AppealsMixin:
    @ensure_connected
    async def is_in_process(self, appeal_id: int) -> bool:
        await self._cursor.execute(
            "SELECT in_process FROM appeals WHERE id = ?",
            (appeal_id,),
        )
        result = await self._cursor.fetchone()
        return bool(result["in_process"]) if result else False

    @ensure_connected
    async def set_in_process(self, appeal_id: int, in_process: bool) -> None:
        await self._cursor.execute(
            "UPDATE appeals SET in_process = ? WHERE id = ?",
            (int(in_process), appeal_id),
        )
        await self.save()

    @ensure_connected
    async def set_reject_reason(self, appeal_id: int, reject_reason: str) -> None:
        await self._cursor.execute(
            "UPDATE appeals SET reject_reason = ? WHERE id = ?",
            (reject_reason, appeal_id),
        )
        await self.save()

    @ensure_connected
    async def is_rejected(self, appeal_id: int) -> bool:
        await self._cursor.execute(
            "SELECT is_rejected FROM appeals WHERE id = ?",
            (appeal_id,),
        )
        result = await self._cursor.fetchone()
        return bool(result["is_rejected"]) if result else False

    @ensure_connected
    async def get_user_id_by_appeal(self, appeal_id: int) -> int:
        await self._cursor.execute(
            "SELECT user_id FROM appeals WHERE id = ?", (appeal_id,)
        )
        result = await self._cursor.fetchone()
        return int(result["user_id"]) if result else 0

    @ensure_connected
    async def create_appeal(
        self,
        tg_id: int,
        category: str,
        message: str,
        photo_id: str,
        latitude: float,
        longitude: float,
    ) -> None:
        await self._cursor.execute(
            """
            INSERT INTO appeals (
                user_id,
                category,
                message,
                reject_reason,
                photo_id,
                latitude,
                longitude
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (tg_id, category, message, "", photo_id, latitude, longitude),
        )
        await self.save()

    @ensure_connected
    async def get_appeal_by_id(
        self,
        appeal_id: int,
    ) -> Optional[Dict[str, Any]]:
        await self._cursor.execute(
            "SELECT * FROM appeals WHERE id = ?",
            (appeal_id,),
        )
        result = await self._cursor.fetchone()
        return dict(result) if result else None

    async def get_user_appeals(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        await self._cursor.execute(
            "SELECT * FROM appeals WHERE user_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (
                user_id,
                limit,
                offset,
            ),
        )
        rows = await self._cursor.fetchall()
        return [dict(row) for row in rows]

    @ensure_connected
    async def get_unmoderated_appeals(
        self,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        await self._cursor.execute(
            """
            SELECT *
            FROM appeals
            WHERE is_accepted = 0 and is_rejected = 0
            ORDER BY created_at ASC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        return [dict(row) for row in await self._cursor.fetchall()]

    @ensure_connected
    async def get_moderated_appeals(
        self,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        await self._cursor.execute(
            """
            SELECT *
            FROM appeals
            WHERE is_accepted = 1
            ORDER BY created_at ASC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        return [dict(row) for row in await self._cursor.fetchall()]

    @ensure_connected
    async def get_rejected_appeals(
        self,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        await self._cursor.execute(
            """
            SELECT *
            FROM appeals
            WHERE is_rejected = 1
            ORDER BY created_at ASC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )
        return [dict(row) for row in await self._cursor.fetchall()]

    @ensure_connected
    async def accept_appeal(self, appeal_id: int) -> None:
        await self._cursor.execute(
            "UPDATE appeals SET is_accepted = 1 WHERE id = ?",
            (appeal_id,),
        )
        await self.save()

    @ensure_connected
    async def reject_appeal(self, appeal_id: int) -> None:
        await self._cursor.execute(
            "UPDATE appeals SET is_rejected = 1 WHERE id = ?",
            (appeal_id,),
        )
        await self.save()

    @ensure_connected
    async def delete_appeal(self, appeal_id: int) -> None:
        await self._cursor.execute(
            "DELETE FROM appeals WHERE id = ?",
            (appeal_id,),
        )
        await self.save()

    @ensure_connected
    async def get_user_appeals_count(self, user_id: int) -> int:
        await self._cursor.execute(
            "SELECT COUNT(*) FROM appeals WHERE user_id = ?", (user_id,)
        )
        result = await self._cursor.fetchone()
        return result[0] if result else 0

    @ensure_connected
    async def get_appeals_count(
        self, is_accepted: Optional[bool] = None, is_rejected: Optional[bool] = None
    ) -> int:
        if is_accepted is None and is_rejected is None:
            await self._cursor.execute(
                "SELECT COUNT(*) FROM appeals",
            )
        else:
            await self._cursor.execute(
                "SELECT COUNT(*) FROM appeals WHERE is_accepted = ? and is_rejected = ?",
                (int(is_accepted), int(is_rejected)),
            )

        result = await self._cursor.fetchone()
        return result[0] if result else 0
