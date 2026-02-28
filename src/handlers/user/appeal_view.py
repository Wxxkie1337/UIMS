import html
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from db import DataBase
from handlers.common import answer
from keyboards.global_kb import Callback, g_main_menu_kb
from keyboards.user_kb import get_switch_kb
from utils import get_user_id

router = Router()
database = DataBase()


class ViewStates(StatesGroup):
    view_appeals = State()


async def get_formatted_text(user_id: int, offset: int, state: FSMContext):
    appeals = await database.get_user_appeals(
        user_id,
        limit=1,
        offset=offset,
    )

    if not appeals:
        return None

    appeal = appeals[0]
    total = await database.get_user_appeals_count(user_id)

    await state.update_data(last_appeal_id=appeal.get("id"))

    status = "🕓 На модерации"
    if appeal.get("is_accepted"):
        status = "📋 В очереди"
    elif appeal.get("in_process"):
        status = "🛠 В работе"
    elif appeal.get("is_rejected"):
        status = "❌ Отклонено"

    reject_block = ""
    if appeal.get("is_rejected"):
        reject_reason = appeal.get("reject_reason") or "Причина не указана."
        reject_block = (
            "\n\n" "❌ <b>Причина отклонения:</b>\n" f"{html.escape(reject_reason)}"
        )

    caption = (
        f"📌 <b>Статус:</b> {status}\n\n"
        f"📅 <b>Дата:</b> {appeal['created_at']}\n"
        f"🗂 <b>Категория:</b> {appeal['category']}\n"
        f"📝 <b>Описание:</b> {appeal['message']}"
        f"{reject_block}"
    )

    return {
        "photo": appeal["photo_id"],
        "caption": caption,
        "reply_markup": get_switch_kb(offset + 1, total),
        "parse_mode": "HTML",
    }


async def switch_appeals(callback: CallbackQuery, state: FSMContext, page: int):
    await callback.answer()
    await callback.message.delete()

    data = await get_formatted_text(get_user_id(callback), page, state)
    if not data:
        await answer(
            text="ℹ️ <b>Обращений пока нет</b>\nСоздайте первое обращение из главного меню.",
            message=callback.message,
            state=state,
            reply_markup=g_main_menu_kb,
        )
        return

    msg = await callback.message.answer_photo(**data)
    await state.update_data(last_bot_message_id=msg.message_id, page=page)


@router.message(ViewStates.view_appeals)
async def handle_delete_messages(message: Message):
    await message.delete()


@router.callback_query(F.data == Callback.VIEW_APPEALS)
async def handle_view_appeals(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ViewStates.view_appeals)
    await switch_appeals(callback, state, 0)


@router.callback_query(F.data == Callback.APPEAL_NEXT)
async def handle_next_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    total = await database.get_user_appeals_count(get_user_id(callback))
    page = await state.get_value("page", None)

    if page is None or page == total - 1:
        return
    page += 1

    await switch_appeals(callback, state, page)


@router.callback_query(F.data == Callback.APPEAL_PREV)
async def handle_prev_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    page = await state.get_value("page", None)

    if page is None or page == 0:
        return
    page -= 1

    await switch_appeals(callback, state, page)


@router.callback_query(F.data == Callback.DELETE_APPEAL)
async def handle_reject_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    last_appeal_id = await state.get_value("last_appeal_id", None)

    if last_appeal_id is None:
        return

    await database.delete_appeal(last_appeal_id)
    await state.update_data(last_appeal_id=None)

    await handle_view_appeals(callback, state)
