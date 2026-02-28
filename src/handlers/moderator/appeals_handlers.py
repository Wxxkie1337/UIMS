from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.common import delete_message
from keyboards.global_kb import Callback, g_view_appeals_kb
from utils import get_chat_id

from .common import database, router, switch_appeals
from .menu_handlers import check_appeals


@router.callback_query(F.data == Callback.M_ACCEPT_APPEAL)
async def accept_appeal(callback: CallbackQuery, state: FSMContext):
    appeal_id = await state.get_value("m_last_appeal_id", None)
    if appeal_id is None:
        return

    await delete_message(
        callback.message.bot,
        get_chat_id(callback),
        await state.get_value("last_bot_message_id"),
    )

    appeal_creator_appeal = await database.get_user_id_by_appeal(appeal_id=appeal_id)
    msg = await callback.message.bot.send_message(
        chat_id=appeal_creator_appeal,
        text=(
            "✅ <b>Обращение принято</b>\n"
            "Модератор проверил заявку и передал ее в работу."
        ),
        reply_markup=g_view_appeals_kb,
    )

    await state.update_data(last_bot_message_id=msg.message_id)
    await database.accept_appeal(appeal_id)

    page = 0
    if p := await state.get_value("m_page"):
        page = max(0, p - 1)

    await check_appeals(callback, state, start_page=page)


@router.callback_query(F.data == Callback.M_APPEAL_NEXT)
async def next_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    page = await state.get_value("m_page") or 0
    next_page = page + 1
    max_page = (
        await database.get_appeals_count(is_accepted=False, is_rejected=False) - 1
    )

    if next_page > max_page or page == max_page:
        return

    await switch_appeals(callback, state, next_page)


@router.callback_query(F.data == Callback.M_APPEAL_PREV)
async def prev_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    page = await state.get_value("m_page") or 0
    prev_page = page - 1

    if prev_page < 0 or page == 0:
        return

    await switch_appeals(callback, state, prev_page)
