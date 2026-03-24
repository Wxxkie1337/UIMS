from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery

from utils.telegram import delete_message


class AutodeleteMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, CallbackQuery):
            return await handler(event, data)

        bot = data.get("bot")
        chat = data.get("event_chat")

        if bot and chat:
            try:
                if hasattr(event.message, "message_id"):
                    await delete_message(bot, chat.id, event.message.message_id)
            except Exception as e:
                print(f"Auto Delete: {e}")
                
        return await handler(event, data)