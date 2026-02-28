from typing import Any, Dict, List, Optional

import aiosqlite

from utils.decorators import ensure_connected, singleton


@singleton
class DataBase:
    async def connect(self, database_path: str) -> None:
        self._connection = await aiosqlite.connect(database_path)
        self._cursor = await self._connection.cursor()
        self._cursor.row_factory = aiosqlite.Row

        await self._cursor.execute("PRAGMA foreign_keys = ON")

        await self._cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                is_banned BOOLEAN DEFAULT 0,
                is_moderator BOOLEAN DEFAULT 0,
                is_administrator BOOLEAN DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS appeals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                in_process BOOLEAN DEFAULT 0,
                is_accepted BOOLEAN DEFAULT 0,
                is_rejected BOOLEAN DEFAULT 0,
                category TEXT,
                message TEXT,
                reject_reason TEXT,
                photo_id TEXT,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES users(tg_id)
            );

            CREATE INDEX IF NOT EXISTS idx_users_tg_id
                ON users(tg_id);

            CREATE INDEX IF NOT EXISTS idx_users_banned
                ON users(is_banned);

            CREATE INDEX IF NOT EXISTS idx_users_moderator
                ON users(is_moderator);

            CREATE INDEX IF NOT EXISTS idx_users_administrator
                ON users(is_administrator);

            CREATE INDEX IF NOT EXISTS idx_appeals_user_id
                ON appeals(user_id);

            CREATE INDEX IF NOT EXISTS idx_appeals_created_at
                ON appeals(created_at);

            CREATE INDEX IF NOT EXISTS idx_appeals_status
                ON appeals(is_accepted, in_process, is_rejected);

            CREATE INDEX IF NOT EXISTS idx_appeals_location
                ON appeals(latitude, longitude);
            """
        )

        await self.save()

    @ensure_connected
    async def close(self) -> None:
        await self._connection.close()

    @ensure_connected
    async def save(self) -> None:
        await self._connection.commit()

    @ensure_connected
    async def add_user(self, tg_id: int) -> None:
        await self._cursor.execute(
            "INSERT OR IGNORE INTO users (tg_id) VALUES (?)",
            (tg_id,),
        )
        await self.save()

    @ensure_connected
    async def is_banned(self, tg_id: int) -> bool:
        await self._cursor.execute(
            "SELECT is_banned FROM users WHERE tg_id = ?",
            (tg_id,),
        )
        result = await self._cursor.fetchone()
        return bool(result["is_banned"]) if result else False

    @ensure_connected
    async def is_moderator(self, tg_id: int) -> bool:
        await self._cursor.execute(
            "SELECT is_moderator FROM users WHERE tg_id = ?",
            (tg_id,),
        )
        result = await self._cursor.fetchone()
        return bool(result["is_moderator"]) if result else False

    @ensure_connected
    async def is_administrator(self, tg_id: int) -> bool:
        await self._cursor.execute(
            "SELECT is_administrator FROM users WHERE tg_id = ?",
            (tg_id,),
        )
        result = await self._cursor.fetchone()
        return bool(result["is_administrator"]) if result else False

    @ensure_connected
    async def ban_user(self, tg_id: int) -> None:
        await self._cursor.execute(
            "UPDATE users SET is_banned = 1 WHERE tg_id = ?",
            (tg_id,),
        )
        await self.save()

    @ensure_connected
    async def unban_user(self, tg_id: int) -> None:
        await self._cursor.execute(
            "UPDATE users SET is_banned = 0 WHERE tg_id = ?",
            (tg_id,),
        )
        await self.save()

    @ensure_connected
    async def make_moderator(self, tg_id: int) -> None:
        await self._cursor.execute(
            "UPDATE users SET is_moderator = 1 WHERE tg_id = ?",
            (tg_id,),
        )
        await self.save()

    @ensure_connected
    async def remove_moderator(self, tg_id: int) -> None:
        await self._cursor.execute(
            "UPDATE users SET is_moderator = 0 WHERE tg_id = ?",
            (tg_id,),
        )
        await self.save()

    @ensure_connected
    async def make_administrator(self, tg_id: int) -> None:
        await self._cursor.execute(
            "UPDATE users SET is_administrator = 1 WHERE tg_id = ?",
            (tg_id,),
        )
        await self.save()

    @ensure_connected
    async def remove_administrator(self, tg_id: int) -> None:
        await self._cursor.execute(
            "UPDATE users SET is_administrator = 0 WHERE tg_id = ?",
            (tg_id,),
        )
        await self.save()

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
            "SELECT user_id FROM appeals WHERE id = ?",
            (appeal_id, )
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
        """await self._cursor.execute(
            "DELETE FROM appeals WHERE id = ?",
            (appeal_id,),
        )"""
        await self._cursor.execute(
            "UPDATE appeals SET is_rejected = 1 WHERE id = ?",
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
        self,
        is_accepted: Optional[bool] = None,
        is_rejected: Optional[bool] = None
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
