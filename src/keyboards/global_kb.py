from enum import StrEnum

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class Callback(StrEnum):
    CREATE_APPEAL = "create_appeal"
    MAIN_MENU = "main_menu"
    MODERATOR_MENU = "moderator_menu"
    ADMIN_MENU = "admin_menu"
    VIEW_APPEALS = "u_view_appeals"
    APPEAL_PREV = "u_appeal_prev"
    APPEAL_NEXT = "u_appeal_next"
    CUSTOM_CATEGORY = "u_custom_category"
    SUCCESS_CREATE_APPEAL = "u_success_create_appeal"
    CANCEL_CREATE_APPEAL = "u_cancel_create_appeal"
    DELETE_APPEAL = "u_delete_appeal"

    M_CHECK_APPEALS = "m_check_appeals"
    M_ACCEPT_APPEAL = "m_accept_appeal"
    M_REJECT_APPEAL = "m_reject_appeal"
    M_APPEAL_PREV = "m_appeal_prev"
    M_APPEAL_NEXT = "m_appeal_next"
    M_ACCEPT_REASON = "m_accept_reason"
    M_CANCEL_REASON = "m_cancel_reason"
    
    A_CHECK_NEW_APPEALS = "a_check_new_appeals"
    A_CHECK_ACTIVE_APPEALS = "a_check_active_appeals"

    EMPTY = "..."
    

g_main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🏠 В главное меню", callback_data=Callback.MAIN_MENU
            )
        ]
    ]
)

g_view_appeals_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📂 Мои обращения", callback_data=Callback.VIEW_APPEALS
            )
        ]
    ]
)

g_understand_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Понятно", callback_data=Callback.MAIN_MENU
            )
        ]
    ]
)


def get_start_kb(is_moderator=False, is_admin=False):
    keyboards = [
        [
            InlineKeyboardButton(
                text="📝 Создать обращение", callback_data=Callback.CREATE_APPEAL,
            )
        ],
        [
            InlineKeyboardButton(
                text="📂 Мои обращения", callback_data=Callback.VIEW_APPEALS,
            )
        ],
    ]
    
    if is_moderator:
        keyboards.append(
            [
                InlineKeyboardButton(
                    text="🛡 Режим модератора", callback_data=Callback.MODERATOR_MENU
                )
            ]
        )
        
    if is_admin:
        keyboards.append(
            [
                InlineKeyboardButton(
                    text="Режим администратора", callback_data=Callback.ADMIN_MENU
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboards)
