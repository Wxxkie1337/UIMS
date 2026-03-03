from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from db import DataBase
from handlers.common import answer, delete_message
from keyboards.moderator_kb import get_unmoderated_appeal_kb, m_menu_kb
from utils import get_chat_id

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
        "caption": (
            f"📅 <b>Дата:</b> {appeal['created_at']}\n"
            f"🗂 <b>Категория:</b> {appeal['category']}\n"
            f"📝 <b>Описание:</b> {appeal['message']}\n"
            f"{geo_block}"
        ),
        "reply_markup": get_unmoderated_appeal_kb(
            offset + 1, total, appeal["latitude"], appeal["longitude"]
        ),
        "parse_mode": "HTML",
    }


async def switch_appeals(callback: CallbackQuery, state: FSMContext, page: int):
    await delete_message(
        callback.message.bot,
        get_chat_id(callback),
        await state.get_value("last_bot_message_id"),
    )

    data = await get_formatted_text(page, state)
    if not data:
        await answer(
            text="ℹ️ <b>Новых обращений пока нет</b>\nВыберите действие в меню модератора.",
            message=callback.message,
            state=state,
            reply_markup=m_menu_kb,
        )
        return

    msg = await callback.message.answer_photo(**data)
    await state.update_data(last_bot_message_id=msg.message_id, m_page=page)
