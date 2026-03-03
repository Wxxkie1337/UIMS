import asyncpg

from utils.decorators import ensure_connected


class ConnectionMixin:
    _connection = None

    async def connect(self, database_url: str) -> None:
        self._connection = await asyncpg.create_pool(dsn=database_url)

        statements = (
            """
            CREATE TABLE IF NOT EXISTS users (
                tg_id BIGINT PRIMARY KEY,
                is_banned BOOLEAN DEFAULT FALSE,
                is_moderator BOOLEAN DEFAULT FALSE,
                is_administrator BOOLEAN DEFAULT FALSE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS appeals (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                in_process BOOLEAN DEFAULT FALSE,
                is_accepted BOOLEAN DEFAULT FALSE,
                is_rejected BOOLEAN DEFAULT FALSE,
                category TEXT,
                message TEXT,
                reject_reason TEXT,
                photo_id TEXT,
                geo_text TEXT,
                latitude DOUBLE PRECISION,
                longitude DOUBLE PRECISION,
                created_at TIMESTAMP DEFAULT NOW(),
                FOREIGN KEY (user_id) REFERENCES users(tg_id)
            )
            """,
            "CREATE INDEX IF NOT EXISTS idx_users_tg_id ON users(tg_id)",
            "CREATE INDEX IF NOT EXISTS idx_users_banned ON users(is_banned)",
            "CREATE INDEX IF NOT EXISTS idx_users_moderator ON users(is_moderator)",
            "CREATE INDEX IF NOT EXISTS idx_users_administrator ON users(is_administrator)",
            "CREATE INDEX IF NOT EXISTS idx_appeals_user_id ON appeals(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_appeals_created_at ON appeals(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_appeals_status ON appeals(is_accepted, in_process, is_rejected)",
            "CREATE INDEX IF NOT EXISTS idx_appeals_location ON appeals(latitude, longitude)",
        )

        async with self._connection.acquire() as conn:
            for statement in statements:
                await conn.execute(statement)

    @ensure_connected
    async def close(self) -> None:
        await self._connection.close()
        self._connection = None

    @ensure_connected
    async def save(self) -> None:
        return None
