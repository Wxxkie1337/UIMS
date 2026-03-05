from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest

from keyboards.global_kb import g_main_menu_kb
from utils import get_chat_id


async def cancel_appeal_flow(message: Message, state: FSMContext):
    """Отменяет обращение если оно существует"""
    if await state.get_state() is not None:
        await delete_message(
            message.bot,
            get_chat_id(message),
            await state.get_value("last_bot_message_id"),
        )
        
        if msg_id := await state.get_value("last_bot_photo_id"):
            await delete_message(message.bot, get_chat_id(message), msg_id)
            
        msg = await message.answer(
            "✅ <b>Обращение отменено</b>\nВы можете вернуться в главное меню и создать новое обращение.",
            reply_markup=g_main_menu_kb,
        )
        
        await state.update_data(last_bot_message_id=msg.message_id)
    else:
        msg = await update_message(
            bot=message.bot,
            chat_id=get_chat_id(message),
            message_id=await state.get_value("last_bot_message_id"),
            text="ℹ️ <b>Активное обращение не найдено</b>\nСейчас отменять нечего."
        )
        await update_last_message(state, msg)


async def answer(text: str, message: Message, state: FSMContext, **kwargs) -> int:
    """Отправляет сообщение сохраняя его id в last_bot_message_id"""
    msg = await message.answer(text, **kwargs)
    await state.update_data(last_bot_message_id=msg.message_id)
    return msg.message_id


async def delete_message(bot, chat_id: int, message_id: int | None) -> None:
    try:
        if not message_id:
            return

        try:
            await bot.delete_message(chat_id, message_id)
        except Exception:
            pass
    except TelegramBadRequest:
        pass


async def update_message(bot: Bot, chat_id, message_id, text=None, photo=None, reply_markup=None):
    try:
        if photo:
            await bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo,
                    caption=text
                ),
                reply_markup=reply_markup
            )
        else:
            await bot.edit_message_text(
                text=text,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=reply_markup
            )
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            return
        
        await delete_message(bot, chat_id, message_id)
        
        if photo:
            msg = await bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=text,
                reply_markup=reply_markup
            )
        else:
            msg = await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup
            )
        
        return msg.message_id
    

async def update_last_message(state, msg_id):
    if msg_id:
        await state.update_data(last_bot_message_id=msg_id)