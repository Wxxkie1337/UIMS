from aiogram import BaseMiddleware

from db import DataBase
from utils.messages import BANNED_ALERT


class BanMiddleware(BaseMiddleware):
    def __init__(self, database: DataBase):
        self.database = database

    async def __call__(self, handler, event, data):
        chat = data.get("event_chat")
        user = data.get("event_from_user")

        if not user or not chat:
            return await handler(event, data)

        user_id = user.id

        if event.message and event.message.text and (event.message.text == "/start" or event.message.text.startswith("/help")):
            return await handler(event, data)

        if await self.database.is_banned(user_id):
            if event.callback_query:
                if event.callback_query.data in {"contact_admin", "understand"}:
                    return await handler(event, data)

                await event.callback_query.answer(BANNED_ALERT, show_alert=True)
                return

            return

        return await handler(event, data)
