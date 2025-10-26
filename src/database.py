import aiosqlite

class DataBase:
    async def connect(self, database_path: str):
        self.connection = await aiosqlite.connect(database_path)
        self.cursor = await self.connection.cursor()
        self.cursor.row_factory = aiosqlite.Row

        await self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER UNIQUE,
                tg_username TEXT,
                
                is_banned BOOLEAN DEFAULT 0,
                is_moderator BOOLEAN DEFAULT 0,
                is_administrator BOOLEAN DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS appeals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                in_process BOOLEAN DEFAULT 0,
                is_accepted BOOLEAN DEFAULT 0,

                category_id INTEGER,
                message TEXT,
                photo_id TEXT,

                latitude REAL NOT NULL,
                longitude REAL NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        await self.save()

    async def add_user(self, tg_id: int, tg_username: str):
        await self.cursor.execute("INSERT OR IGNORE INTO users (tg_id, tg_username) VALUES (?, ?)", (tg_id, tg_username))
        await self.save()
        
    async def ban_user(self, tg_id: int):
        await self.cursor.execute("UPDATE users SET is_banned = 1 WHERE tg_id = ?", (tg_id, ))
        await self.save()

    async def unban_user(self, tg_id: int):
        await self.cursor.execute("UPDATE users SET is_banned = 0 WHERE tg_id = ?", (tg_id, ))
        await self.save()

    async def make_moderator(self, tg_id: int):
        await self.cursor.execute("UPDATE users SET is_moderator = 1 WHERE tg_id = ?", (tg_id, ))
        await self.save()

    async def make_administrator(self, tg_id: int):
        await self.cursor.execute("UPDATE users SET is_administrator = 1 WHERE tg_id = ?", (tg_id, ))
        await self.save()

    async def remove_moderator(self, tg_id: int):
        await self.cursor.execute("UPDATE users SET is_moderator = 0 WHERE tg_id = ?", (tg_id, ))
        await self.save()

    async def remove_administrator(self, tg_id: int):
        await self.cursor.execute("UPDATE users SET is_administrator = 0 WHERE tg_id = ?", (tg_id, ))
        await self.save()

    async def is_moderator(self, tg_id: int) -> bool:
        await self.cursor.execute("SELECT is_moderator FROM users WHERE tg_id = ?", (tg_id, ))
        result = await self.cursor.fetchone()
        return result['is_moderator'] == 1 if result else False
    
    async def is_administrator(self, tg_id: int) -> bool:
        await self.cursor.execute("SELECT is_administrator FROM users WHERE tg_id = ?", (tg_id, ))
        result = await self.cursor.fetchone()
        return result['is_administrator'] == 1 if result else False

    async def create_appeal(self, tg_id: int, category_id: int, message: str, photo_id: str, latitude: float, longitude: float):
        await self.cursor.execute(
        """ INSERT INTO appeals (user_id, category_id, message, photo_id, latitude, longitude)
            VALUES (?, ?, ?, ?, ?, ?) """, 
            (tg_id, category_id, message, photo_id, latitude, longitude)
        )
        await self.save()

    async def get_appeal_by_id(self, appeal_id: int) -> dict | None:
        """
        **Ключи словаря**: id, user_id, in_process, is_accepted, category_id, message, photo_id, latitude, longitude, created_at\n
        **Если не найдено**: None
        """
        await self.cursor.execute("SELECT * FROM appeals WHERE id = ?", (appeal_id, ))
        return await self.cursor.fetchone()

    async def get_unmoderated_appeals(self) -> list[dict | None]:
        """
        **Ключи словаря**: id, user_id, in_process, is_accepted, category_id, message, photo_id, latitude, longitude, created_at\n
        """
        await self.cursor.execute("SELECT * FROM appeals WHERE is_accepted = 0 ORDER BY created_at ASC")
        return await self.cursor.fetchall()

    async def get_moderated_appeals(self) -> list[dict]:
        """
        **Ключи словаря**: id, user_id, in_process, is_accepted, category_id, message, photo_id, latitude, longitude, created_at\n
        """
        await self.cursor.execute("SELECT * FROM appeals WHERE is_accepted = 1 ORDER BY created_at ASC")
        return await self.cursor.fetchall()

    async def accept_appeal(self, appeal_id: int):
        await self.cursor.execute("UPDATE appeals SET is_accepted = 1 WHERE id = ?", (appeal_id, ))
        await self.save()

    async def reject_appeal(self, appeal_id: int):
        await self.cursor.execute("DELETE FROM appeals WHERE id = ?", (appeal_id, ))
        await self.save()

    async def save(self):
        await self.connection.commit()
    
    async def close(self):
        await self.connection.close()