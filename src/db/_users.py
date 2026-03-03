from utils.decorators import ensure_connected


class UsersMixin:
    @ensure_connected
    async def add_user(self, tg_id: int) -> None:
        await self._connection.execute(
            "INSERT INTO users (tg_id) VALUES ($1) ON CONFLICT (tg_id) DO NOTHING",
            tg_id,
        )

    @ensure_connected
    async def is_banned(self, tg_id: int) -> bool:
        result = await self._connection.fetchrow(
            "SELECT is_banned FROM users WHERE tg_id = $1",
            tg_id,
        )
        return bool(result["is_banned"]) if result else False

    @ensure_connected
    async def is_moderator(self, tg_id: int) -> bool:
        result = await self._connection.fetchrow(
            "SELECT is_moderator FROM users WHERE tg_id = $1",
            tg_id,
        )
        return bool(result["is_moderator"]) if result else False

    @ensure_connected
    async def is_administrator(self, tg_id: int) -> bool:
        result = await self._connection.fetchrow(
            "SELECT is_administrator FROM users WHERE tg_id = $1",
            tg_id,
        )
        return bool(result["is_administrator"]) if result else False

    @ensure_connected
    async def ban_user(self, tg_id: int) -> None:
        await self._connection.execute(
            "UPDATE users SET is_banned = TRUE WHERE tg_id = $1",
            tg_id,
        )

    @ensure_connected
    async def unban_user(self, tg_id: int) -> None:
        await self._connection.execute(
            "UPDATE users SET is_banned = FALSE WHERE tg_id = $1",
            tg_id,
        )

    @ensure_connected
    async def make_moderator(self, tg_id: int) -> None:
        await self._connection.execute(
            "UPDATE users SET is_moderator = TRUE WHERE tg_id = $1",
            tg_id,
        )

    @ensure_connected
    async def remove_moderator(self, tg_id: int) -> None:
        await self._connection.execute(
            "UPDATE users SET is_moderator = FALSE WHERE tg_id = $1",
            tg_id,
        )

    @ensure_connected
    async def make_administrator(self, tg_id: int) -> None:
        await self._connection.execute(
            "UPDATE users SET is_administrator = TRUE WHERE tg_id = $1",
            tg_id,
        )

    @ensure_connected
    async def remove_administrator(self, tg_id: int) -> None:
        await self._connection.execute(
            "UPDATE users SET is_administrator = FALSE WHERE tg_id = $1",
            tg_id,
        )
