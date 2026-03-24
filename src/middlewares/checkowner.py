from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from keyboards.global_kb import Callback
from config import OWNERS_ID
from utils.messages import ACCESS_DENIED_ALERT

UNRESOLVED_EVENTS = {
    Callback.O_GENERATE_ROLE_URL,
    Callback.O_ROLE,
    Callback.O_BAN_STATE,
    Callback.O_CHOOSE_EMPLOYEES,
    Callback.O_MANAGE_EMPLOYEES,
    Callback.O_NEXT_PAGE,
    Callback.O_PREV_PAGE,
    Callback.O_REMOVE_ROLE,
    Callback.O_EMPLOYER_INFO,
    Callback.OWNER_MENU
}

class CheckOwner(BaseMiddleware):    
    async def __call__(self, handler, event, data):
        user = data.get("event_from_user")

        if user and user.id not in OWNERS_ID:
            if isinstance(event, CallbackQuery) and (event.data.startswith("o_") or event.data == Callback.OWNER_MENU):
                await event.answer(ACCESS_DENIED_ALERT, show_alert=True)
                return
        return await handler(event, data)
