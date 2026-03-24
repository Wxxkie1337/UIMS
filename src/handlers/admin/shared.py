from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

from db import DataBase

from utils.misc import get_user_link, format_datetime
from utils.messages import (
    LABEL_APPEAL_NUMBER,
    LABEL_CATEGORY,
    LABEL_DATE,
    LABEL_DESCRIPTION,
    LABEL_USER,
)

router = Router()
database = DataBase()


class AdminStates(StatesGroup):
    check_moderated_appeals = State()
    check_defer_appeals = State()
    check_active_appeals = State()
    reject_reason = State()
    wait_reason = State()
    complete_message = State()


def get_formatted_text(appeal, kb):
    user_id = appeal.get("user_id")
    username = appeal.get("username")
    
    user_link = get_user_link(user_id, username)

    return {
        "photo": appeal.get("media_id") if appeal.get("media_type") == "photo" else None,
        "video": appeal.get("media_id") if appeal.get("media_type") == "video" else None,
        "text": (
            f"{LABEL_USER.format(user_link)}\n\n"
            f"{LABEL_APPEAL_NUMBER} {appeal['id']}\n"
            f"{LABEL_DATE} {format_datetime(appeal['created_at'])}\n"
            f"{LABEL_CATEGORY} {appeal['category']}\n"
            f"{LABEL_DESCRIPTION} {appeal['message']}"
        ),
        "reply_markup": kb
    }
