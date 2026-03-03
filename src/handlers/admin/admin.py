from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from db import DataBase
from keyboards.global_kb import Callback, g_understand_kb
from keyboards.admin_kb import a_menu_kb
from handlers.common import answer, delete_message
from utils import get_chat_id, get_user_id


router = Router()
database = DataBase()


@router.callback_query(F.data == Callback.ADMIN_MENU)
async def admin_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    user_id = get_user_id(callback)
    chat_id = get_chat_id(callback)
    
    last_msg_id = await state.get_value("last_bot_message_id")
    
    await delete_message(
        bot=callback.message.bot,
        chat_id=chat_id,
        message_id=last_msg_id
    )
    
    if not await database.is_administrator(user_id):
        await answer(
            text="⛔ <b>Недостаточно прав</b>\nРежим администратора доступен только назначенным администраторам.",
            message=callback.message,
            state=state,
            reply_markup=g_understand_kb
        )
        return
    
    await answer(
        text="<b>Меню администратора</b>\nВыберите действие.",
        message=callback.message,
        state=state,
        reply_markup=a_menu_kb
    )
