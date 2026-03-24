from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.global_kb import Callback
from utils.misc import get_map_url
from utils.messages import (
    APPEAL_NEXT,
    APPEAL_PREV,
    CONFIRM,
    GOOGLE_MAPS,
    MAIN_MENU,
    MODERATOR_ACCEPT_APPEAL,
    MODERATOR_NEW_APPEALS,
    MODERATOR_REJECT_APPEAL,
    PAGE_INDICATOR,
    REASON_CANCEL,
    YANDEX_MAPS,
)


m_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=MODERATOR_NEW_APPEALS,
                callback_data=Callback.M_CHECK_APPEALS,
            )
        ],
        [
            InlineKeyboardButton(
                text=MAIN_MENU,
                callback_data=Callback.MAIN_MENU,
            )
        ],
    ]
)

m_confirm_reason_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=CONFIRM,
                callback_data=Callback.M_ACCEPT_REASON,
            ),
            InlineKeyboardButton(
                text=REASON_CANCEL,
                callback_data=Callback.M_CANCEL_REASON,
            ),
        ]
    ]
)


def get_unmoderated_appeal_kb(
    offset: int,
    total_appeals: int,
    latitude: float,
    longitude: float,
):
    keyboards = [
        [
            InlineKeyboardButton(
                text=APPEAL_PREV,
                callback_data=Callback.M_APPEAL_PREV,
            ),
            InlineKeyboardButton(
                text=PAGE_INDICATOR.format(current=offset, total=total_appeals),
                callback_data=Callback.EMPTY,
            ),
            InlineKeyboardButton(
                text=APPEAL_NEXT,
                callback_data=Callback.M_APPEAL_NEXT,
            ),
        ]
    ]

    if latitude and longitude:
        keyboards.append(
            [
                InlineKeyboardButton(
                    text=GOOGLE_MAPS,
                    url=get_map_url("google", latitude, longitude),
                ),
                InlineKeyboardButton(
                    text=YANDEX_MAPS,
                    url=get_map_url("yandex", latitude, longitude),
                ),
            ]
        )

    keyboards.append(
        [
            InlineKeyboardButton(
                text=MODERATOR_ACCEPT_APPEAL,
                callback_data=Callback.M_ACCEPT_APPEAL,
            ),
            InlineKeyboardButton(
                text=MODERATOR_REJECT_APPEAL,
                callback_data=Callback.M_REJECT_APPEAL,
            ),
        ]
    )
    keyboards.append(
        [
            InlineKeyboardButton(
                text=MAIN_MENU,
                callback_data=Callback.MAIN_MENU,
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboards)
