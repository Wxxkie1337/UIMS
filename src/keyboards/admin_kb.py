from enum import StrEnum

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from keyboards.global_kb import Callback
from utils import get_map_url


a_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📂 Новые обращения", callback_data=Callback.A_CHECK_NEW_APPEALS
            ),
        ],
        [
            InlineKeyboardButton(
                text="📂 Активные обращения", callback_data=Callback.A_CHECK_ACTIVE_APPEALS
            ),
        ],
        [
            InlineKeyboardButton(
                text="🏠 В главное меню", callback_data=Callback.MAIN_MENU
            )
        ]
    ]
)