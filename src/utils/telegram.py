from aiogram.types import CallbackQuery, Message


def get_user_id(event: Message | CallbackQuery) -> int:
    return event.from_user.id


def get_chat_id(event: Message | CallbackQuery) -> int:
    return event.chat.id if isinstance(event, Message) else event.message.chat.id
