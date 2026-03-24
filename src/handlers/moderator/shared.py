from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from db import DataBase
from keyboards.moderator_kb import get_unmoderated_appeal_kb, m_menu_kb
from utils.misc import format_datetime, get_user_link
from utils.telegram import (
    update_last_message,
    UIContext
)
from utils.messages import (
    LABEL_APPEAL_NUMBER,
    LABEL_USER,
    LABEL_ADDRESS,
    LABEL_CATEGORY,
    LABEL_DATE,
    LABEL_DESCRIPTION,
    MODERATOR_NO_APPEALS_TEXT,
)

router = Router()
database = DataBase()


class ModeratorStates(StatesGroup):
    default = State()
    moderator_view = State()
    input_reason = State()
    wait_reason_state = State()


async def get_formatted_text(offset: int, state: FSMContext):
    appeals = await database.get_unmoderated_appeals(limit=1, offset=offset)
    if not appeals:
        return None

    appeal = appeals[0]
    total = await database.get_appeals_count()
    await state.update_data(m_last_appeal_id=appeal["id"])

    address_block = ""
    if appeal.get("geo_text"):
        address_block = f"\n{LABEL_ADDRESS} {appeal['geo_text']}"
        
    user_id = appeal.get("user_id")
    username = appeal.get("username")
    
    user_link = get_user_link(
        user_id=user_id,
        username=username
    )

    return {
        "photo": appeal["media_id"],
        "text": (
            f"{LABEL_USER.format(user_link)}\n\n"
            f"{LABEL_APPEAL_NUMBER} {appeal['id']}\n"
            f"{LABEL_DATE} {format_datetime(appeal['created_at'])}\n"
            f"{LABEL_CATEGORY} {appeal['category']}\n"
            f"{LABEL_DESCRIPTION} {appeal['message']}"
            f"{address_block}"
        ),
        "reply_markup": get_unmoderated_appeal_kb(
            offset + 1,
            total,
            appeal["latitude"],
            appeal["longitude"],
        ),
    }


async def switch_appeals(callback: CallbackQuery, state: FSMContext, page: int):
    ctx = await UIContext.from_callback(callback, database)
    data = await get_formatted_text(page, state)

    if not data:
        msg = await ctx.update_message(
            text=MODERATOR_NO_APPEALS_TEXT,
            reply_markup=m_menu_kb,
        )
        await update_last_message(ctx.db, ctx.user_id, msg)
        return

    msg = await ctx.update_message(**data)
    await update_last_message(ctx.db, ctx.user_id, msg)
    await state.update_data(m_page=page)


async def appeal_is_new(state: FSMContext):
    appeal_id = await state.get_value("m_last_appeal_id")
    if appeal_id is None:
        return False
    
    appeal = await database.get_appeal_by_id(appeal_id)

    if appeal and appeal.get("status") == 'new':
        return True
    return False
