import asyncpg


class ConnectionMixin:
    _connection = None

    async def connect(self, database_url: str) -> None:
        self._connection = await asyncpg.create_pool(dsn=database_url)

        async with self._connection.acquire() as conn:
            await conn.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_type WHERE typname = 'appeal_status'
                    ) THEN
                        CREATE TYPE appeal_status AS ENUM (
                            'new',
                            'in_process',
                            'accepted',
                            'rejected',
                            'completed',
                            'deferred'
                        );
                    END IF;
                END
                $$;
            """)

            await conn.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_type WHERE typname = 'role_names'
                    ) THEN
                        CREATE TYPE role_names AS ENUM (
                            'admin',
                            'moderator'
                        );
                    END IF;
                END
                $$;
            """)


            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    tg_id BIGINT PRIMARY KEY,
                    username TEXT,
                    is_banned BOOLEAN DEFAULT FALSE,
                    last_ui_message_id BIGINT,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS moderators (
                    tg_id BIGINT PRIMARY KEY
                        REFERENCES users(tg_id) ON DELETE CASCADE,
                    accepted_appeals INTEGER DEFAULT 0,
                    rejected_appeals INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS admins (
                    tg_id BIGINT PRIMARY KEY
                        REFERENCES users(tg_id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS appeals (
                    id BIGSERIAL PRIMARY KEY,
                    
                    user_id BIGINT NOT NULL
                        REFERENCES users(tg_id) ON DELETE CASCADE,
                    username TEXT,

                    status appeal_status DEFAULT 'new',
                    deferred_by BIGINT,
                    in_process_by BIGINT,

                    category TEXT,
                    message TEXT,

                    resolution_message TEXT,

                    geo_text TEXT,
                    latitude DOUBLE PRECISION,
                    longitude DOUBLE PRECISION,

                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS medias (
                    id SERIAL PRIMARY KEY,
                    appeal_id BIGINT
                        REFERENCES appeals(id) ON DELETE CASCADE,
                    media_id TEXT NOT NULL,
                    media_type TEXT NOT NULL,
                    sender_type TEXT NOT NULL
                )
            """)

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS role_invites (
                    token TEXT UNIQUE NOT NULL,
                    role role_names NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)


            await conn.execute("CREATE INDEX IF NOT EXISTS idx_users_banned ON users(is_banned)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_moderators_tg_id ON moderators(tg_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_admins_tg_id ON admins(tg_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_appeals_user_id ON appeals(user_id)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_appeals_created_at ON appeals(created_at)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_appeals_status ON appeals(status)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_appeals_location ON appeals(latitude, longitude)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_medias_appeal_id ON medias(appeal_id)")


            await conn.execute("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW()
            """)

            await conn.execute("""
                ALTER TABLE appeals
                ADD COLUMN IF NOT EXISTS deferred_by BIGINT
            """)

            await conn.execute("""
                ALTER TABLE appeals
                ADD COLUMN IF NOT EXISTS in_process_by BIGINT
            """)
            
            await conn.execute("""
                ALTER TABLE appeals
                ADD COLUMN IF NOT EXISTS resolution_message TEXT
            """)

            await conn.execute("""
                ALTER TABLE medias
                ADD COLUMN IF NOT EXISTS media_type TEXT
            """)
