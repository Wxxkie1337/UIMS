import aiosqlite
from typing import Optional, List, Dict, Any

def ensure_connected(func):
    async def wrapper(self, *args, **kwargs):
        if self._connection is None:
            raise RuntimeError(
                "База данных не подключена. Вызовите метод connect() перед использованием."
            )
        return await func(self, *args, **kwargs)
    return wrapper

class DataBase:
    # Подключение и управление соединением

    async def connect(self, database_path: str) -> None:
        """Подключается к SQLite-базе и создаёт таблицы при необходимости.

        Аргументы:
            database_path (str): Путь к файлу базы данных.
        """
        self._connection = await aiosqlite.connect(database_path)
        self._cursor = await self._connection.cursor()
        self._cursor.row_factory = aiosqlite.Row

        await self._cursor.execute("PRAGMA foreign_keys = ON")

        await self._cursor.executescript("""
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
                category_id INTEGER,
                message TEXT,
                photo_id TEXT,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                         
                FOREIGN KEY (user_id) REFERENCES users(tg_id)
            );

            CREATE INDEX IF NOT EXISTS idx_users_tg_id ON users(tg_id);
            CREATE INDEX IF NOT EXISTS idx_users_banned ON users(is_banned);
            CREATE INDEX IF NOT EXISTS idx_users_moderator ON users(is_moderator);
            CREATE INDEX IF NOT EXISTS idx_users_administrator ON users(is_administrator);

            CREATE INDEX IF NOT EXISTS idx_appeals_user_id ON appeals(user_id);
            CREATE INDEX IF NOT EXISTS idx_appeals_created_at ON appeals(created_at);
            CREATE INDEX IF NOT EXISTS idx_appeals_status ON appeals(is_accepted, in_process);
            CREATE INDEX IF NOT EXISTS idx_appeals_category ON appeals(category_id);
            CREATE INDEX IF NOT EXISTS idx_appeals_location ON appeals(latitude, longitude);
        """)

        await self.save()

    @ensure_connected
    async def close(self) -> None:
        """Закрывает соединение с базой данных."""
        await self._connection.close()

    @ensure_connected
    async def save(self) -> None:
        """Фиксирует текущие изменения в базе данных."""
        await self._connection.commit()

    # Управление пользователями

    @ensure_connected
    async def add_user(self, tg_id: int) -> None:
        """Добавляет нового пользователя в базу (игнорирует дубликаты по tg_id).

        Аргументы:
            tg_id (int): Уникальный Telegram ID пользователя.
        """
        await self._cursor.execute("INSERT OR IGNORE INTO users (tg_id) VALUES (?)", (tg_id,))
        await self.save()
        
    @ensure_connected
    async def is_banned(self, tg_id: int) -> bool:
        """Проверяет, забанен ли пользователь.

        Аргументы:
            tg_id (int): Telegram ID пользователя.

        Возвращает:
            bool: True, если пользователь забанен, иначе False.
        """
        await self._cursor.execute("SELECT is_banned FROM users WHERE tg_id = ?", (tg_id,))
        result = await self._cursor.fetchone()
        return bool(result["is_banned"]) if result else False

    @ensure_connected
    async def is_moderator(self, tg_id: int) -> bool:
        """Проверяет, является ли пользователь модератором.

        Аргументы:
            tg_id (int): Telegram ID пользователя.

        Возвращает:
            bool: True, если пользователь — модератор, иначе False.
        """
        await self._cursor.execute("SELECT is_moderator FROM users WHERE tg_id = ?", (tg_id,))
        result = await self._cursor.fetchone()
        return bool(result["is_moderator"]) if result else False

    @ensure_connected
    async def is_administrator(self, tg_id: int) -> bool:
        """Проверяет, является ли пользователь администратором.

        Аргументы:
            tg_id (int): Telegram ID пользователя.

        Возвращает:
            bool: True, если пользователь — администратор, иначе False.
        """
        await self._cursor.execute("SELECT is_administrator FROM users WHERE tg_id = ?", (tg_id,))
        result = await self._cursor.fetchone()
        return bool(result["is_administrator"]) if result else False

    @ensure_connected
    async def ban_user(self, tg_id: int) -> None:
        """Блокирует пользователя.

        Аргументы:
            tg_id (int): Telegram ID пользователя.
        """
        await self._cursor.execute("UPDATE users SET is_banned = 1 WHERE tg_id = ?", (tg_id,))
        await self.save()

    @ensure_connected
    async def unban_user(self, tg_id: int) -> None:
        """Разблокирует пользователя.

        Аргументы:
            tg_id (int): Telegram ID пользователя.
        """
        await self._cursor.execute("UPDATE users SET is_banned = 0 WHERE tg_id = ?", (tg_id,))
        await self.save()

    @ensure_connected
    async def make_moderator(self, tg_id: int) -> None:
        """Назначает пользователя модератором.

        Аргументы:
            tg_id (int): Telegram ID пользователя.
        """
        await self._cursor.execute("UPDATE users SET is_moderator = 1 WHERE tg_id = ?", (tg_id,))
        await self.save()

    @ensure_connected
    async def remove_moderator(self, tg_id: int) -> None:
        """Лишает пользователя прав модератора.

        Аргументы:
            tg_id (int): Telegram ID пользователя.
        """
        await self._cursor.execute("UPDATE users SET is_moderator = 0 WHERE tg_id = ?", (tg_id,))
        await self.save()

    @ensure_connected
    async def make_administrator(self, tg_id: int) -> None:
        """Назначает пользователя администратором.

        Аргументы:
            tg_id (int): Telegram ID пользователя.
        """
        await self._cursor.execute("UPDATE users SET is_administrator = 1 WHERE tg_id = ?", (tg_id,))
        await self.save()

    @ensure_connected
    async def remove_administrator(self, tg_id: int) -> None:
        """Лишает пользователя прав администратора.

        Аргументы:
            tg_id (int): Telegram ID пользователя.
        """
        await self._cursor.execute("UPDATE users SET is_administrator = 0 WHERE tg_id = ?", (tg_id,))
        await self.save()

    # Работа с обращениями

    @ensure_connected
    async def is_in_process(self, appeal_id: int) -> bool:
        """Проверяет, в процессе выполнения ли обращение.

        Аргументы:
            appeal_id (int): ID обращения.

        Возвращает:
            bool: True, если обращение в процессе выполнения, иначе False.
        """
        await self._cursor.execute("SELECT in_process FROM appeals WHERE id = ?", (appeal_id, ))
        result = await self._cursor.fetchone()
        return bool(result["in_process"]) if result else False

    @ensure_connected
    async def create_appeal(
        self,
        tg_id: int,
        category_id: int,
        message: str,
        photo_id: str,
        latitude: float,
        longitude: float
    ) -> None:
        """Создаёт новое обращение от пользователя.

        Аргументы:
            tg_id (int): Telegram ID автора обращения.
            category_id (int): ID категории обращения.
            message (str): Текст сообщения.
            photo_id (str): File ID фотографии в Telegram.
            latitude (float): Широта геолокации.
            longitude (float): Долгота геолокации.
        """
        await self._cursor.execute(
            """INSERT INTO appeals (user_id, category_id, message, photo_id, latitude, longitude)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (tg_id, category_id, message, photo_id, latitude, longitude)
        )
        await self.save()

    @ensure_connected
    async def get_appeal_by_id(self, appeal_id: int) -> Optional[Dict[str, Any]]:
        """Возвращает обращение по его ID.

        Аргументы:
            appeal_id (int): Уникальный идентификатор обращения.

        Возвращает:
            dict | None: Словарь с данными обращения или None, если не найдено.
        """
        await self._cursor.execute("SELECT * FROM appeals WHERE id = ?", (appeal_id,))
        result = await self._cursor.fetchone()
        return dict(result) if result else None

    @ensure_connected
    async def get_unmoderated_appeals(self) -> List[Dict[str, Any]]:
        """Возвращает все непринятые (неодобренные) обращения.

        Возвращает:
            list[dict]: Список обращений в хронологическом порядке (от старых к новым).
        """
        await self._cursor.execute("SELECT * FROM appeals WHERE is_accepted = 0 ORDER BY created_at ASC")

        result = await self._cursor.fetchall()
        return [dict(appeal) for appeal in result]

    @ensure_connected
    async def get_moderated_appeals(self) -> List[Dict[str, Any]]:
        """Возвращает все одобренные обращения.

        Возвращает:
            list[dict]: Список обращений в хронологическом порядке (от старых к новым).
        """
        await self._cursor.execute("SELECT * FROM appeals WHERE is_accepted = 1 ORDER BY created_at ASC")

        result = await self._cursor.fetchall()
        return [dict(appeal) for appeal in result]

    @ensure_connected
    async def accept_appeal(self, appeal_id: int) -> None:
        """Одобряет обращение (помечает как accepted).

        Аргументы:
            appeal_id (int): ID обращения.
        """
        await self._cursor.execute("UPDATE appeals SET is_accepted = 1 WHERE id = ?", (appeal_id,))
        await self.save()

    @ensure_connected
    async def reject_appeal(self, appeal_id: int) -> None:
        """Отклоняет и удаляет обращение из базы.

        Аргументы:
            appeal_id (int): ID обращения.
        """
        await self._cursor.execute("DELETE FROM appeals WHERE id = ?", (appeal_id,))
        await self.save()