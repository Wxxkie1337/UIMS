from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from db import DataBase


class AddUser(BaseMiddleware):
    def __init__(self, database: DataBase):
        self.database = database
        
    async def __call__(self, handler, event, data):
        database = self.database
        user = data.get("event_from_user") or getattr(event, "from_user", None)
        
        if user:
            await database.add_user(user.id, user.username)
        return await handler(event, data)
