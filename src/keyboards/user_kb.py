from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from utils.misc import get_map_url
from utils.messages import (
    APPEAL_NEXT,
    APPEAL_PREV,
    BACK_BUTTON,
    CANCEL,
    CONFIRM,
    CUSTOM_CATEGORY,
    DELETE_APPEAL,
    GOOGLE_MAPS,
    LOCATION,
    MAIN_MENU,
    PAGE_INDICATOR,
    USER_APPEAL_DETAILS_BUTTON,
    USER_CATEGORY_OPTIONS,
    YANDEX_MAPS,
)
from keyboards.global_kb import Callback


u_info_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=BACK_BUTTON, callback_data=Callback.U_BACK_TO_APPEAL
            )
        ]
    ]
)


def get_switch_kb(offset: int, max_appeals: int, is_completed: bool) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=APPEAL_PREV, callback_data=Callback.APPEAL_PREV
            ),
            InlineKeyboardButton(
                text=PAGE_INDICATOR.format(current=offset, total=max_appeals),
                callback_data=Callback.EMPTY,
            ),
            InlineKeyboardButton(
                text=APPEAL_NEXT, callback_data=Callback.APPEAL_NEXT
            ),
        ]
    ]

    if is_completed:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=USER_APPEAL_DETAILS_BUTTON,
                    callback_data=Callback.CHECK_INFO,
                )
            ]
        )

    keyboard.extend([
        [
            InlineKeyboardButton(
                text=DELETE_APPEAL, callback_data=Callback.DELETE_APPEAL
            )
        ],
        [
            InlineKeyboardButton(
                text=MAIN_MENU, callback_data=Callback.MAIN_MENU
            )
        ],
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_category_kb(row_size: int = 2) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []

    for text, value in USER_CATEGORY_OPTIONS:
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
                text=CUSTOM_CATEGORY,
                callback_data=Callback.CUSTOM_CATEGORY,
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_finish_kb(latitude: float = None, longitude: float = None) -> InlineKeyboardMarkup:
    keyboards = []
    
    if latitude and longitude:
        keyboards.append([
            InlineKeyboardButton(
                text=GOOGLE_MAPS,
                url=get_map_url("google", latitude, longitude),
            ),
            InlineKeyboardButton(
                text=YANDEX_MAPS,
                url=get_map_url("yandex", latitude, longitude),
            ),
        ])
    
    keyboards.append([
        InlineKeyboardButton(
            text=CANCEL,
            callback_data=Callback.CANCEL_CREATE_APPEAL,
        ),
        InlineKeyboardButton(
            text=CONFIRM,
            callback_data=Callback.SUCCESS_CREATE_APPEAL,
        ),
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboards)
