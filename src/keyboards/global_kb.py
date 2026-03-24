from enum import StrEnum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.messages import (
    ADMIN_MODE,
    CREATE_APPEAL,
    MAIN_MENU,
    MODERATOR_MODE,
    OWNER_MODE,
    UNDERSTAND,
    VIEW_APPEALS,
)


class Callback(StrEnum):
    CREATE_APPEAL = "create_appeal"
    MAIN_MENU = "main_menu"
    MODERATOR_MENU = "moderator_menu"
    ADMIN_MENU = "admin_menu"
    OWNER_MENU = "owner_menu"
    VIEW_APPEALS = "u_view_appeals"
    APPEAL_PREV = "u_appeal_prev"
    APPEAL_NEXT = "u_appeal_next"
    CUSTOM_CATEGORY = "u_custom_category"
    SUCCESS_CREATE_APPEAL = "u_success_create_appeal"
    CANCEL_CREATE_APPEAL = "u_cancel_create_appeal"
    DELETE_APPEAL = "u_delete_appeal"
    UNDERSTAND = "understand"
    CHECK_INFO = "u_check_info"
    U_BACK_TO_APPEAL = "u_back_to_appeal"

    M_CHECK_APPEALS = "m_check_appeals"
    M_CHECK_ACCEPTED_APPEALS = "m_check_accepted_appeals"
    M_ACCEPT_APPEAL = "m_accept_appeal"
    M_REJECT_APPEAL = "m_reject_appeal"
    M_APPEAL_PREV = "m_appeal_prev"
    M_APPEAL_NEXT = "m_appeal_next"
    M_ACCEPT_REASON = "m_accept_reason"
    M_CANCEL_REASON = "m_cancel_reason"

    A_CHECK_MODERATED_APPEALS = "a_check_moderated_appeals"
    A_CHECK_ACTIVE_APPEALS = "a_check_active_appeals"
    A_ACCEPT_APPEAL = "a_accept_appeal"
    A_REJECT_APPEAL = "a_reject_appeal"
    A_TO_WORK = "a_to_work"
    A_PAGE = "a_page"
    A_CHECK_DEFER_APPEALS = "a_check_defer_appeals"
    A_DEFER_APPEAL = "a_defer_appeal"
    A_NEXT_MESSAGE = "a_next_message"
    A_ACCEPT_REASON = "a_accept_reason"
    A_REJECT_REASON = "a_reject_reason"
    A_BACK_TO_APPEALS = "a_back_to_appeals"
    A_COMPLETE_APPEAL = "a_complete_appeal"
    A_CANCEL = "a_cancel"
    A_SUCCESS = "a_success"
    A_BACK_TO_DEFERRED = "a_back_to_deferred"
    A_BACK_TO_ACTIVE = "a_back_to_active"

    O_GENERATE_ROLE_URL = "o_generate_role_url"
    O_ROLE = "o_role"
    O_MANAGE_EMPLOYEES = "o_manage_employees"
    O_CHOOSE_EMPLOYEES = "o_choose_employees"
    O_NEXT_PAGE = "o_next_page"
    O_PREV_PAGE = "o_prev_page"
    O_EMPLOYER_INFO = "o_employer_info"
    O_REMOVE_ROLE = "o_remove_role"
    O_BAN_STATE = "o_ban_state"
    O_APPEALS_HISTORY = "o_appeals_history"
    O_BAN_USER = "o_ban_user"
    O_BAN_HISTORY = "o_ban_history"
    O_USER_INFO = "o_user_info"
    O_UNBAN_USER = "o_unban_user"

    EMPTY = "..."


g_main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=MAIN_MENU,
                callback_data=Callback.MAIN_MENU,
            )
        ]
    ]
)

g_view_appeals_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=VIEW_APPEALS,
                callback_data=Callback.VIEW_APPEALS,
            )
        ]
    ]
)

g_understand_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=UNDERSTAND,
                callback_data=Callback.UNDERSTAND,
            )
        ]
    ]
)


def get_start_kb(is_moderator=False, is_admin=False, is_owner=False):
    keyboards = [
        [
            InlineKeyboardButton(
                text=CREATE_APPEAL,
                callback_data=Callback.CREATE_APPEAL,
            )
        ],
        [
            InlineKeyboardButton(
                text=VIEW_APPEALS,
                callback_data=Callback.VIEW_APPEALS,
            )
        ],
    ]
    
    keyboard_part = []

    if is_moderator:
        keyboard_part.append(
            
                InlineKeyboardButton(
                    text=MODERATOR_MODE,
                    callback_data=Callback.MODERATOR_MENU,
                )
            
        )

    if is_admin:
        keyboard_part.append(
            
                InlineKeyboardButton(
                    text=ADMIN_MODE,
                    callback_data=Callback.ADMIN_MENU,
                )
            
        )
    
    if keyboard_part:
        keyboards.append(keyboard_part)

    if is_owner:
        keyboards.append(
            [
                InlineKeyboardButton(
                    text=OWNER_MODE,
                    callback_data=Callback.OWNER_MENU,
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboards)
