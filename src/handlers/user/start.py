from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from db import DataBase
from handlers.common import cancel_appeal_flow, delete_message, answer, update_last_message, update_message
from keyboards.global_kb import Callback, get_start_kb
from utils import get_chat_id, get_user_id
from config import OWNER_ID

router = Router()
database = DataBase()


@router.message(Command("start"))
async def handle_start_command(message: Message, state: FSMContext):
    user_id = get_user_id(message)
    if user_id == int(OWNER_ID):
        await database.make_administrator(user_id)
        await database.make_moderator(user_id)
        
    is_moderator = await database.is_moderator(user_id)
    is_admin = await database.is_administrator(user_id)

    msg = await message.answer(
        "<b>Добро пожаловать в помощник ЖК «Янино-1»</b>\n\n"
        "Здесь вы можете отправить обращение по проблемам на территории комплекса: "
        "утечки, мусор, освещение и другие вопросы.",
        reply_markup=get_start_kb(is_moderator=is_moderator, is_admin=is_admin),
    )

    await state.update_data(last_bot_message_id=msg.message_id)
    await database.add_user(get_user_id(message))


@router.callback_query(F.data == Callback.MAIN_MENU)
async def handle_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    is_moderator = await database.is_moderator(get_user_id(callback))
    is_admin = await database.is_administrator(get_user_id(callback))

    msg = await update_message(
        bot=callback.message.bot,
        chat_id=get_chat_id(callback),
        message_id=await state.get_value("last_bot_message_id"),
        text=(
            "<b>Главное меню</b>\n\n"
            "Выберите действие: создайте новое обращение или проверьте ранее отправленные."
        ),
        reply_markup=get_start_kb(is_moderator=is_moderator, is_admin=is_admin)
    )
    await update_last_message(state, msg)


@router.message(Command("cancel"))
async def handle_cancel_command(message: Message, state: FSMContext):
    await message.delete()
    await cancel_appeal_flow(message, state)


@router.callback_query(F.data == Callback.EMPTY)
async def handle_empty(callback: CallbackQuery):
    await callback.answer()
