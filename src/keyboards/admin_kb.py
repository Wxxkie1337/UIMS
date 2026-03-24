from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from keyboards.global_kb import Callback
from utils.messages import (
    ADMIN_ACTIVE_APPEALS,
    ADMIN_APPROVED_APPEALS,
    ADMIN_CANCEL_BUTTON,
    ADMIN_COMPLETE_BUTTON,
    ADMIN_DEFERRED_APPEALS,
    ADMIN_DEFER_BUTTON,
    ADMIN_MENU_BUTTON,
    ADMIN_REASON_BACK_BUTTON,
    ADMIN_REASON_CANCEL_BUTTON,
    ADMIN_REASON_CONFIRM_BUTTON,
    ADMIN_REJECT_BUTTON,
    ADMIN_RETURN_TO_DEFERRED_BUTTON,
    ADMIN_RETURN_TO_MODERATED_BUTTON,
    ADMIN_TAKE_TO_WORK_BUTTON,
    APPEAL_PREV,
    APPEAL_NEXT,
    CANCEL,
    MAIN_MENU,
    PAGE_INDICATOR,
)


a_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=ADMIN_APPROVED_APPEALS, callback_data=Callback.A_CHECK_MODERATED_APPEALS
            ),
        ],
        [
            InlineKeyboardButton(
                text=ADMIN_DEFERRED_APPEALS, callback_data=Callback.A_CHECK_DEFER_APPEALS
            )
        ],
        [
            InlineKeyboardButton(
                text=ADMIN_ACTIVE_APPEALS, callback_data=Callback.A_CHECK_ACTIVE_APPEALS
            ),
        ],
        [
            InlineKeyboardButton(
                text=MAIN_MENU, callback_data=Callback.MAIN_MENU
            )
        ]
    ]
)


a_adminmenu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=ADMIN_MENU_BUTTON,
                callback_data=Callback.ADMIN_MENU
            )
        ]
    ]
)


a_cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=ADMIN_CANCEL_BUTTON,
                callback_data=Callback.A_CANCEL
            )
        ]
    ]
)

a_cancel_or_success_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=CANCEL,
                callback_data=Callback.A_CANCEL
            ),
            InlineKeyboardButton(
                text=ADMIN_REASON_CONFIRM_BUTTON,
                callback_data=Callback.A_SUCCESS
            )
        ]
    ]
)


def get_new_appeals_kb(page, max_page, appeal_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=APPEAL_PREV,
                    callback_data=f"{Callback.A_PAGE}!{page - 1}",
                ),
                InlineKeyboardButton(
                    text=PAGE_INDICATOR.format(current=page + 1, total=max_page + 1),
                    callback_data=Callback.EMPTY,
                ),
                InlineKeyboardButton(
                    text=APPEAL_NEXT,
                    callback_data=f"{Callback.A_PAGE}!{page+1}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ADMIN_TAKE_TO_WORK_BUTTON,
                    callback_data=f"{Callback.A_TO_WORK}!{appeal_id}"
                ),
                InlineKeyboardButton(
                    text=ADMIN_DEFER_BUTTON,
                    callback_data=f"{Callback.A_DEFER_APPEAL}!{appeal_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=ADMIN_REJECT_BUTTON,
                    callback_data=f"{Callback.A_REJECT_APPEAL}!{appeal_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ADMIN_MENU_BUTTON,
                    callback_data=Callback.ADMIN_MENU
                )
            ]
        ]
    )


def get_deferred_appeals_kb(page, max_page, appeal_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=APPEAL_PREV,
                    callback_data=f"{Callback.A_PAGE}!{page - 1}",
                ),
                InlineKeyboardButton(
                    text=PAGE_INDICATOR.format(current=page + 1, total=max_page + 1),
                    callback_data=Callback.EMPTY,
                ),
                InlineKeyboardButton(
                    text=APPEAL_NEXT,
                    callback_data=f"{Callback.A_PAGE}!{page+1}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ADMIN_TAKE_TO_WORK_BUTTON,
                    callback_data=f"{Callback.A_TO_WORK}!{appeal_id}"
                ),
                InlineKeyboardButton(
                    text=ADMIN_REJECT_BUTTON,
                    callback_data=f"{Callback.A_REJECT_APPEAL}!{appeal_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ADMIN_MENU_BUTTON,
                    callback_data=Callback.ADMIN_MENU
                )
            ]
        ]
    )


def get_active_appeals_kb(page, max_page, appeal_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=APPEAL_PREV,
                    callback_data=f"{Callback.A_PAGE}!{page - 1}",
                ),
                InlineKeyboardButton(
                    text=PAGE_INDICATOR.format(current=page + 1, total=max_page + 1),
                    callback_data=Callback.EMPTY,
                ),
                InlineKeyboardButton(
                    text=APPEAL_NEXT,
                    callback_data=f"{Callback.A_PAGE}!{page+1}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ADMIN_COMPLETE_BUTTON,
                    callback_data=f"{Callback.A_COMPLETE_APPEAL}!{appeal_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=ADMIN_RETURN_TO_DEFERRED_BUTTON,
                    callback_data=f"{Callback.A_BACK_TO_DEFERRED}!{appeal_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=ADMIN_RETURN_TO_MODERATED_BUTTON,
                    callback_data=f"{Callback.A_BACK_TO_ACTIVE}!{appeal_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=ADMIN_MENU_BUTTON,
                    callback_data=Callback.ADMIN_MENU
                )
            ]
        ]
    )


def get_reason_kb(stage, appeal_id):
    inline_keyboard = []
    
    if stage == 1:
        inline_keyboard.append([
            InlineKeyboardButton(
                text=ADMIN_REASON_CANCEL_BUTTON,
                callback_data=Callback.UNDERSTAND
            ),
            InlineKeyboardButton(
                text=ADMIN_REASON_CONFIRM_BUTTON,
                callback_data=f"{Callback.A_ACCEPT_REASON}!{appeal_id}"
            )
        ])
    elif stage == 2:
        inline_keyboard.append([
            InlineKeyboardButton(
                text=ADMIN_REASON_BACK_BUTTON,
                callback_data=Callback.A_BACK_TO_APPEALS
            )
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
