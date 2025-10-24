import aiosqlite

class DataBase:
    async def connect(self, database_path: str):
        self.connection = await aiosqlite.connect(database_path)
        self.cursor = await self.connection.cursor()

        await self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                tg_username TEXT,
                tg_id INTEGER UNIQUE,
                
                is_moderator BOOL,
                is_administrator BOOL
            );
            
            CREATE TABLE IF NOT EXISTS appeals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                in_process BOOL,
                accepted BOOL,

                group_id INTEGER,
                message TEXT,
                photo_id TEXT,

                latitude REAL NOT NULL,
                longitude REAL NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        await self._save()

    async def _save(self):
        await self.connection.commit()
    
    async def _close(self):
        await self.connection.close()