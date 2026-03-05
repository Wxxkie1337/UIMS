from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InputMediaPhoto

from db import DataBase
from keyboards.global_kb import Callback, g_understand_kb
from keyboards.admin_kb import a_menu_kb
from handlers.common import update_message, update_last_message
from utils import get_chat_id, get_user_id


router = Router()
database = DataBase()


@router.callback_query(F.data == Callback.ADMIN_MENU)
async def admin_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    user_id = get_user_id(callback)
    chat_id = get_chat_id(callback)
    
    last_msg_id = await state.get_value("last_bot_message_id")
    
    if not await database.is_administrator(user_id):
        msg_id = await update_message(
            bot=callback.message.bot,
            chat_id=chat_id,
            message_id=last_msg_id,
            text="⛔ <b>Недостаточно прав</b>\nРежим администратора доступен только назначенным администраторам.",
            reply_markup=g_understand_kb
        )
        await update_last_message(state, msg_id)
        return
     
    msg_id = await update_message(
        bot=callback.message.bot,
        chat_id=chat_id,
        message_id=last_msg_id,
        text="<b>Меню администратора</b>\nВыберите действие.",
        reply_markup=a_menu_kb
        )
    await update_last_message(state, msg_id)


@router.callback_query(F.data == Callback.A_CHECK_NEW_APPEALS)
async def check_new_appeals(callback: CallbackQuery, state=FSMContext):
    await callback.answer()
    