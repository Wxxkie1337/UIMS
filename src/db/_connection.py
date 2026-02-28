import aiosqlite

from utils.decorators import ensure_connected


class ConnectionMixin:
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
