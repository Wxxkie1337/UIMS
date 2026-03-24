from typing import Any, Dict, List, Optional

from utils.decorators import ensure_connected


class MediasMixin:
    @ensure_connected
    async def get_media_by_id(self, media_id: int) -> Optional[Dict[str, Any]]:
        result = await self._connection.fetchrow(
            """
            SELECT * FROM medias
            WHERE medias.media_id = $1
            LIMIT 1
            """,
            media_id
        )
        return dict(result) if result else None
    
    @ensure_connected
    async def get_user_media_by_id(self, media_id: int) -> Optional[Dict[str, Any]]:
        result = await self._connection.fetchrow(
            """
            SELECT * FROM medias
            WHERE medias.media_id = $1 AND medias.sender_type = 'user'
            LIMIT 1
            """,
            media_id
        )
        return dict(result) if result else None
    
    @ensure_connected
    async def get_admin_media_by_id(self, media_id: int) -> Optional[Dict[str, Any]]:
        result = await self._connection.fetchrow(
            """
            SELECT * FROM medias
            WHERE medias.media_id = $1 AND medias.sender_type = 'admin'
            LIMIT 1
            """,
            media_id
        )
        return dict(result) if result else None
    
    @ensure_connected
    async def get_admin_media_by_appeal_id(self, appeal_id: int) -> Optional[Dict[str, Any]]:
        result = await self._connection.fetchrow(
            """
            SELECT * FROM medias
            WHERE medias.appeal_id = $1 AND medias.sender_type = 'admin'
            LIMIT 1
            """,
            appeal_id
        )
        return dict(result) if result else {}
    
    @ensure_connected
    async def add_media(self, appeal_id: int, media_id: int, media_type: str, sender_type: int) -> bool:
        result = await self._connection.fetchval(
            """
            INSERT INTO medias (appeal_id, media_id, media_type, sender_type)
            VALUES ($1, $2, $3, $4)
            RETURNING appeal_id
            """,
            appeal_id, media_id, media_type, sender_type,
        )
        return result is not None
        
