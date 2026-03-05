from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from db import DataBase
from handlers.common import update_last_message, update_message
from keyboards.moderator_kb import get_unmoderated_appeal_kb, m_menu_kb
from utils import get_chat_id, format_datetime

router = Router()
database = DataBase()


class ModeratorStates(StatesGroup):
    moderator_view = State()
    input_reason = State()


async def get_formatted_text(offset: int, state: FSMContext):
    appeals = await database.get_unmoderated_appeals(
        limit=1,
        offset=offset,
    )

    if not appeals:
        return None

    appeal = appeals[0]
    total = await database.get_appeals_count(is_accepted=False, is_rejected=False)

    await state.update_data(m_last_appeal_id=appeal.get("id"))
    
    geo_block = ""
    if appeal.get("geo_text"):
        geo_block = f"📍 <b>Адрес:</b> {appeal.get('geo_text')}"

    return {
        "photo": appeal["photo_id"],
        "text": (
            f"📅 <b>Дата:</b> {format_datetime(appeal['created_at'])}\n"
            f"🗂 <b>Категория:</b> {appeal['category']}\n"
            f"📝 <b>Описание:</b> {appeal['message']}\n"
            f"{geo_block}"
        ),
        "reply_markup": get_unmoderated_appeal_kb(
            offset + 1, total, appeal["latitude"], appeal["longitude"]
        )
    }


async def switch_appeals(callback: CallbackQuery, state: FSMContext, page: int):
    chat_id = get_chat_id(callback)
    last_msg_id = await state.get_value("last_bot_message_id")
    data = await get_formatted_text(page, state)

    if not data:
        msg = await update_message(
            bot=callback.message.bot,
            chat_id=chat_id,
            message_id=last_msg_id,
            text="ℹ️ <b>Новых обращений пока нет</b>\nВыберите действие в меню модератора.",
            reply_markup=m_menu_kb
        )
        await update_last_message(state, msg)
        return

    msg = await update_message(
        bot=callback.message.bot,
        chat_id=chat_id,
        message_id=last_msg_id,
        **data
    )
    
    await update_last_message(state, msg)
    await state.update_data(m_page=page)
