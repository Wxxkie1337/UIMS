from typing import Any, Dict, List, Optional

from utils.decorators import ensure_connected


class AppealsMixin:
    @ensure_connected
    async def get_user_id_by_appeal(self, appeal_id: int) -> Optional[int]:
        result = await self._connection.fetchval(
            "SELECT user_id FROM appeals WHERE id = $1",
            appeal_id,
        )
        return int(result) if result else None

    @ensure_connected
    async def create_appeal(
        self,
        tg_id: int,
        username: str,
        category: str,
        message: str,
        media_id: str,
        media_type: str,
        geo_text: str = None,
        latitude: float = None,
        longitude: float = None,
    ) -> None:
        async with self._connection.acquire() as conn:
            async with conn.transaction():
                appeal_id = await conn.fetchval(
                    """
                    INSERT INTO appeals (
                        user_id,
                        username,
                        category,
                        message,
                        resolution_message,
                        geo_text,
                        latitude,
                        longitude
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    RETURNING id
                    """,
                    tg_id,
                    username,
                    category,
                    message,
                    None,
                    geo_text,
                    latitude,
                    longitude,
                )

                await conn.execute(
                    """
                    INSERT INTO medias (appeal_id, media_id, media_type, sender_type)
                    VALUES ($1, $2, $3, $4)
                    """,
                    appeal_id,
                    media_id,
                    media_type,
                    "user",
                )

    @ensure_connected
    async def get_appeal_by_id(
        self,
        appeal_id: int,
    ) -> Optional[Dict[str, Any]]:
        result = await self._connection.fetchrow(
            f"""SELECT appeals.*, 
            (
                SELECT medias.media_id
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_id,
            (
                SELECT medias.media_type
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_type
            FROM appeals WHERE appeals.id = $1""",
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
            f"""
            SELECT appeals.*,  
            (
                SELECT medias.media_id
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_id,
            (
                SELECT medias.media_type
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_type
            FROM appeals
            WHERE appeals.user_id = $1
            ORDER BY appeals.created_at DESC
            LIMIT $2 OFFSET $3
            """,
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
            f"""
            SELECT appeals.*,  
            (
                SELECT medias.media_id
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_id,
            (
                SELECT medias.media_type
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_type
            FROM appeals
            WHERE appeals.status = 'new'
            ORDER BY appeals.created_at ASC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        return [dict(row) for row in rows]
    
    @ensure_connected
    async def get_active_appeals(
        self,
        admin_id: int,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            f"""
            SELECT appeals.*, users.is_banned, users.last_ui_message_id, users.created_at AS user_created_at,  
            (
                SELECT medias.media_id
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_id,
            (
                SELECT medias.media_type
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_type
            FROM appeals
            JOIN users ON users.tg_id = appeals.user_id
            WHERE appeals.status = 'in_process' and users.is_banned = FALSE and appeals.in_process_by = $1
            ORDER BY appeals.created_at ASC
            LIMIT $2 OFFSET $3
            """,
            admin_id,
            limit,
            offset
        )
        return [dict(row) for row in rows]
    
    @ensure_connected
    async def get_active_appeals_count(self, admin_id) -> int:
        return await self._connection.fetchval(
            """
            SELECT COUNT(*)
            FROM appeals
            JOIN users ON users.tg_id = appeals.user_id
            WHERE appeals.status = 'in_process' and appeals.in_process_by = $1
            AND users.is_banned = FALSE
            """,
            admin_id
        )
    
    @ensure_connected
    async def get_deferred_appeals(
        self,
        deferred_by_id,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            f"""
            SELECT appeals.*, users.is_banned, users.last_ui_message_id, users.created_at AS user_created_at,  
            (
                SELECT medias.media_id
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_id,
            (
                SELECT medias.media_type
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_type
            FROM appeals
            JOIN users ON users.tg_id = appeals.user_id
            WHERE appeals.status = 'deferred' and users.is_banned = FALSE and appeals.deferred_by = $1
            ORDER BY appeals.created_at ASC
            LIMIT $2 OFFSET $3
            """,
            deferred_by_id,
            limit,
            offset
        )
        return [dict(row) for row in rows]
    
    @ensure_connected
    async def get_deferred_appeals_count(self, admin_id) -> int:
        return await self._connection.fetchval(
            """
            SELECT COUNT(*)
            FROM appeals
            JOIN users ON users.tg_id = appeals.user_id
            WHERE appeals.status = 'deferred' and appeals.deferred_by = $1
            AND users.is_banned = FALSE
            """,
            admin_id
        )

    @ensure_connected
    async def get_moderated_appeals(
        self,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            f"""
            SELECT appeals.*, users.is_banned, users.last_ui_message_id, users.created_at AS user_created_at,  
            (
                SELECT medias.media_id
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_id,
            (
                SELECT medias.media_type
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_type
            FROM appeals
            JOIN users ON users.tg_id = appeals.user_id
            WHERE appeals.status = 'accepted' and users.is_banned = FALSE
            ORDER BY appeals.created_at ASC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        return [dict(row) for row in rows]
    
    @ensure_connected
    async def get_moderated_appeals_count(self) -> int:
        return await self._connection.fetchval(
            """
            SELECT COUNT(*)
            FROM appeals
            JOIN users ON users.tg_id = appeals.user_id
            WHERE appeals.status = 'accepted'
            AND users.is_banned = FALSE
            """
        )

    @ensure_connected
    async def get_rejected_appeals(
        self,
        offset: int,
        limit: int,
    ) -> List[Dict[str, Any]]:
        rows = await self._connection.fetch(
            f"""
            SELECT appeals.*,  
            (
                SELECT medias.media_id
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_id,
            (
                SELECT medias.media_type
                FROM medias
                WHERE medias.appeal_id = appeals.id AND medias.sender_type = 'user'
                ORDER BY medias.id ASC
                LIMIT 1
            ) AS media_type
            FROM appeals
            JOIN users ON users.tg_id = appeals.user_id
            WHERE appeals.status = 'rejected' AND users.is_banned = FALSE
            ORDER BY appeals.created_at ASC
            LIMIT $1 OFFSET $2
            """,
            limit,
            offset,
        )
        return [dict(row) for row in rows]

    @ensure_connected
    async def accept_appeal(self, appeal_id: int) -> bool:
        result = await self._connection.fetchval(
            """
            UPDATE appeals
            SET status = 'accepted'
            WHERE id = $1 AND status = 'new'
            RETURNING id
            """,
            appeal_id,
        )
        return result is not None

    @ensure_connected
    async def set_appeal_status(self, appeal_id: int, status: str, **kwargs) -> bool:
        statuses = ['new', 'in_process', 'accepted', 'rejected', 'completed', 'deferred']
        
        if status not in statuses:
            raise ValueError(
                f"set_appeal_status: Некорректный статус, список доступных статусов: {', '.join(statuses)}"
            )

        set_parts = ["status = $1"]
        values = [status]

        for i, (key, value) in enumerate(kwargs.items(), start=2):
            set_parts.append(f"{key} = ${i}")
            values.append(value)

        query = f"""
            UPDATE appeals
            SET {', '.join(set_parts)}
            WHERE id = ${len(values) + 1}
            RETURNING id
        """

        values.append(appeal_id)

        result = await self._connection.fetchval(query, *values)
        return result is not None

    @ensure_connected
    async def reject_appeal(self, appeal_id: int, reject_reason: str) -> bool:
        result = await self._connection.fetchval(
            """
            UPDATE appeals
            SET status = 'rejected',
                resolution_message = $1
            WHERE id = $2
            RETURNING id
            """,
            reject_reason,
            appeal_id
        )
        return result is not None
    
    @ensure_connected
    async def process_appeal(self, admin_id: int, appeal_id: int) -> bool:
        result = await self._connection.fetchval(
            """
            UPDATE appeals
            SET status = 'in_process',
                in_process_by = $1
            WHERE id = $2
            RETURNING id
            """,
            admin_id, appeal_id
        )
        return result is not None
    
    @ensure_connected
    async def defer_appeal(self, admin_id: int, appeal_id: int) -> bool:
        result = await self._connection.fetchval(
            """
            UPDATE appeals
            SET status = 'deferred',
                deferred_by = $1
            WHERE id = $2
            RETURNING id
            """,
            admin_id, appeal_id
        )
        return result is not None
    
    @ensure_connected
    async def complete_appeal(self, appeal_id: int, message: str) -> bool:
        result = await self._connection.fetchval(
            """
            UPDATE appeals
            SET status = 'completed',
                resolution_message = $1
            WHERE id = $2
            RETURNING id
            """,
            message, appeal_id
        )
        return result is not None

    @ensure_connected
    async def delete_appeal(self, appeal_id: int) -> None:
        await self._connection.execute(
            "DELETE FROM appeals WHERE id = $1",
            appeal_id,
        )

    @ensure_connected
    async def get_user_appeals_count(self, user_id: int) -> int:
        result = await self._connection.fetchval(
            "SELECT COUNT(*) AS total FROM appeals WHERE user_id = $1",
            user_id,
        )
        return result

    @ensure_connected
    async def get_appeals_count(self, total: bool = False) -> int:
        if total:
            result = await self._connection.fetchval(
                "SELECT COUNT(*) FROM appeals",
            )
        else:
            result = await self._connection.fetchval(
                "SELECT COUNT(*) FROM appeals WHERE status = 'new'",
            )

        return result
    
    @ensure_connected
    async def get_rejected_appeals_count(self) -> int:
        return await self._connection.fetchval(
            """
            SELECT COUNT(*)
            FROM appeals
            JOIN users ON users.tg_id = appeals.user_id
            WHERE appeals.status = 'rejected'
            AND users.is_banned = FALSE
            """
        )
