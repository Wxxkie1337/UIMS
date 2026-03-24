import html

from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

from db import DataBase
from utils.messages import (
    LABEL_APPEAL_NUMBER,
    LABEL_CATEGORY,
    LABEL_DATE,
    LABEL_DESCRIPTION,
    LABEL_REJECT_REASON,
    LABEL_USER,
    REJECT_REASON_EMPTY,
)
from utils.misc import get_user_link, format_datetime
from keyboards.owner_kb import get_appeals_kb

router = Router()
database = DataBase()


class OwnerStates(StatesGroup):
    manage_employees = State()
    appeals_history = State()
    bans_history = State()


async def get_formatted_text(page: int, max_page: int):
    if page < 0 or page > max_page: 
        return None
    
    appeals = await database.get_rejected_appeals(page, 1)
    if not appeals:
        return None

    appeal = appeals[0]
        
    user_id = appeal.get("user_id")
    username = appeal.get("username")
    
    user_link = get_user_link(user_id, username)
    

    reject_reason = appeal.get("reject_reason") or REJECT_REASON_EMPTY
    reject_block = (
        f"\n\n{LABEL_REJECT_REASON}\n{html.escape(reject_reason)}"
    )

    return {
        "photo": appeal["media_id"],
        "text": (
            f"{LABEL_USER.format(user_link)}\n\n"
            f"{LABEL_APPEAL_NUMBER} {appeal['id']}\n"
            f"{LABEL_DATE} {format_datetime(appeal['created_at'])}\n"
            f"{LABEL_CATEGORY} {appeal['category']}\n"
            f"{LABEL_DESCRIPTION} {appeal['message']}"
            f"{reject_block}"
        ),
        "reply_markup": get_appeals_kb(user_id, page, max_page)
    }
