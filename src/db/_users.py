from utils.decorators import ensure_connected


class UsersMixin:
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
