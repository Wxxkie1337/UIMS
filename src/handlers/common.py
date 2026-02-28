from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
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
        await state.clear()
        msg = await message.answer(
            "Обращение отменено. Всего доброго! 👋",
            reply_markup=g_main_menu_kb,
        )
        await state.update_data(last_bot_message_id=msg.message_id)
    else:
        await answer(
            text="Нет активного обращения.",
            message=message,
            state=state
        )


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