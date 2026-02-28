from enum import StrEnum

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from utils.misc import get_map_url
from keyboards.global_kb import Callback


CATEGORIES = [
    ("🚧 Дороги и тротуары", "Дороги"),
    ("🗑 Мусор и уборка", "Мусор"),
    ("💡 Освещение", "Освещение"),
    ("🚰 Вода / Канализация", "Вода"),
    ("🏠 Дом и подъезд", "Дом"),
    ("🚗 Парковка", "Парковка"),
    ("🐕 Животные", "Животные"),
    ("👥 Соседи / люди", "Люди"),
]


u_location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="📍 Отправить текущее местоположение",
                request_location=True,
            )
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def get_switch_kb(offset: int, max_appeals: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад", callback_data=Callback.APPEAL_PREV
                ),
                InlineKeyboardButton(
                    text=f"📄 {offset}/{max_appeals}", callback_data=Callback.EMPTY
                ),
                InlineKeyboardButton(
                    text="Вперёд ➡️", callback_data=Callback.APPEAL_NEXT
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏠 В главное меню", callback_data=Callback.MAIN_MENU
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Удалить обращение", callback_data=Callback.DELETE_APPEAL
                )
            ],
        ]
    )


def get_category_kb(row_size: int = 2) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []

    for text, value in CATEGORIES:
        row.append(
            InlineKeyboardButton(
                text=text,
                callback_data=f"category_{value}",
            )
        )
        if len(row) == row_size:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append(
        [
            InlineKeyboardButton(
                text="✏️ Свой вариант",
                callback_data=Callback.CUSTOM_CATEGORY,
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_finish_kb(latitude: float, longitude: float) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
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
                    text="❌ Отменить",
                    callback_data=Callback.CANCEL_CREATE_APPEAL,
                ),
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data=Callback.SUCCESS_CREATE_APPEAL,
                ),
            ],
        ]
    )
