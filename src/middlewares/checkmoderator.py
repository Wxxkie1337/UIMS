from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from db import DataBase
from keyboards.global_kb import Callback
from utils.messages import ACCESS_DENIED_ALERT


class CheckModerator(BaseMiddleware):
    def __init__(self, database: DataBase):
        self.database = database
        
    async def __call__(self, handler, event, data):
        database: DataBase = self.database
        user = data.get("event_from_user")
        
        if user and not await database.is_moderator(user.id):
            if isinstance(event, CallbackQuery) and (event.data.startswith("m_") or event.data == Callback.MODERATOR_MENU):
                await event.answer(ACCESS_DENIED_ALERT, show_alert=True)
                return
        return await handler(event, data)
