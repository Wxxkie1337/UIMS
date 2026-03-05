from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.common import update_last_message, update_message
from keyboards.global_kb import Callback, g_understand_kb
from keyboards.moderator_kb import m_menu_kb
from utils import get_chat_id, get_user_id

from .common import ModeratorStates, database, router, switch_appeals


@router.callback_query(F.data == Callback.MODERATOR_MENU)
async def handle_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    user_id = get_user_id(callback)
    chat_id = get_chat_id(callback)

    last_bot_message_id = await state.get_value("last_bot_message_id")

    await state.set_state(ModeratorStates.moderator_view)

    if not await database.is_moderator(user_id):
        msg = await update_message(
            bot=callback.message.bot,
            chat_id=chat_id,
            message_id=last_bot_message_id,
            text="⛔ <b>Недостаточно прав</b>\nРежим модератора доступен только назначенным сотрудникам.",
            reply_markup=g_understand_kb
        )
        await update_last_message(state, msg)
        return
    
    msg = await update_message(
        bot=callback.message.bot,
        chat_id=chat_id,
        message_id=last_bot_message_id,
        text="<b>Меню модератора</b>\nВыберите действие.",
        reply_markup=m_menu_kb
    )
    await update_last_message(state, msg)
 

@router.callback_query(F.data == Callback.M_CHECK_APPEALS)
async def check_appeals(callback: CallbackQuery, state: FSMContext, *, start_page=0):
    await state.update_data(m_page=start_page)
    await callback.answer()
    await switch_appeals(callback, state, start_page)
