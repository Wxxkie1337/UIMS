from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.common import answer, delete_message
from keyboards.global_kb import Callback, g_main_menu_kb
from keyboards.moderator_kb import m_menu_kb
from utils import get_chat_id, get_user_id

from .common import ModeratorStates, database, router, switch_appeals


@router.callback_query(F.data == Callback.MODERATOR_MENU)
async def handle_menu(callback: CallbackQuery, state: FSMContext, *, del_msg=True):
    await callback.answer()

    user_id = get_user_id(callback)
    chat_id = get_chat_id(callback)

    callback_message_id = callback.message.message_id if callback.message else None
    last_bot_message_id = await state.get_value("last_bot_message_id")

    await state.set_state(ModeratorStates.moderator_view)

    if del_msg:
        await delete_message(callback.bot, chat_id, callback_message_id)
        if last_bot_message_id != callback_message_id:
            await delete_message(callback.bot, chat_id, last_bot_message_id)

    if callback_message_id or last_bot_message_id:
        await state.update_data(last_bot_message_id=None)

    if not await database.is_moderator(user_id):
        await answer(
            text="⛔ <b>Недостаточно прав</b>\nРежим модератора доступен только назначенным сотрудникам.",
            message=callback.message,
            state=state,
            reply_markup=g_main_menu_kb,
        )
        return

    await answer(
        text="<b>Меню модератора</b>\nВыберите действие.",
        message=callback.message,
        state=state,
        reply_markup=m_menu_kb,
    )


@router.callback_query(F.data == Callback.M_CHECK_APPEALS)
async def check_appeals(callback: CallbackQuery, state: FSMContext, *, start_page=0):
    await state.update_data(m_page=start_page)
    await callback.answer()
    await switch_appeals(callback, state, start_page)
