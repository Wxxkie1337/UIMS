from enum import StrEnum

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from keyboards.global_kb import Callback
from utils import get_map_url


m_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📂 Новые обращения", callback_data=Callback.M_CHECK_APPEALS
            )
        ],
        [
            InlineKeyboardButton(
                text="🏠 В главное меню", callback_data=Callback.MAIN_MENU
            )
        ],
    ]
)

m_confirm_reason_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="✅ Подтвердить", callback_data=Callback.M_ACCEPT_REASON
            ),
            InlineKeyboardButton(
                text="↩️ Отменить", callback_data=Callback.M_CANCEL_REASON
            ),
        ]
    ]
)


def get_unmoderated_appeal_kb(
    offset: int, total_appeals: int, latitude: float, longitude: float
):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад", callback_data=Callback.M_APPEAL_PREV
                ),
                InlineKeyboardButton(
                    text=f"📄 {offset}/{total_appeals}", callback_data=Callback.EMPTY
                ),
                InlineKeyboardButton(
                    text="➡️ Вперёд", callback_data=Callback.M_APPEAL_NEXT
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🗺 Google Maps",
                    url=get_map_url("google", latitude, longitude),
                ),
                InlineKeyboardButton(
                    text="🟡 Яндекс Карты",
                    url=get_map_url("yandex", latitude, longitude),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✅ Принять", callback_data=Callback.M_ACCEPT_APPEAL
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить", callback_data=Callback.M_REJECT_APPEAL
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏠 В главное меню", callback_data=Callback.MAIN_MENU
                )
            ],
        ]
    )
