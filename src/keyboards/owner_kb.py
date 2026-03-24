from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.global_kb import Callback
from utils.messages import (
    APPEAL_NEXT,
    APPEAL_PREV,
    MAIN_MENU,
    OWNER_ADMIN_ROLE_BUTTON,
    OWNER_APPEALS_BUTTON,
    OWNER_BAN_AUTHOR_BUTTON,
    OWNER_BAN_BUTTON,
    OWNER_BANS_BUTTON,
    OWNER_EMPLOYEES_ADMINS_BUTTON,
    OWNER_EMPLOYEES_BUTTON,
    OWNER_EMPLOYEES_MODERATORS_BUTTON,
    OWNER_EMPLOYEE_MANAGER_BUTTON,
    OWNER_GENERATE_ROLE_BUTTON,
    OWNER_MENU_BUTTON,
    OWNER_MODERATOR_ROLE_BUTTON,
    OWNER_REMOVE_ROLE_BUTTON,
    OWNER_UNBAN_BUTTON,
    PAGE_INDICATOR,
)


o_ownermenu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=OWNER_MENU_BUTTON,
                callback_data=Callback.OWNER_MENU,
            )
        ]
    ]
)


o_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=OWNER_GENERATE_ROLE_BUTTON,
                callback_data=Callback.O_GENERATE_ROLE_URL,
            )
        ],
        [
            InlineKeyboardButton(
                text=OWNER_EMPLOYEES_BUTTON,
                callback_data=Callback.O_MANAGE_EMPLOYEES,
            )
        ],
        [
            InlineKeyboardButton(
                text=OWNER_APPEALS_BUTTON,
                callback_data=Callback.O_APPEALS_HISTORY,
            ),
            InlineKeyboardButton(
                text=OWNER_BANS_BUTTON,
                callback_data=Callback.O_BAN_HISTORY,
            ),
        ],
        [
            InlineKeyboardButton(
                text=MAIN_MENU,
                callback_data=Callback.MAIN_MENU,
            )
        ],
    ]
)

o_roles_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=OWNER_MODERATOR_ROLE_BUTTON,
                callback_data=Callback.O_ROLE + "!moderator",
            )
        ],
        [
            InlineKeyboardButton(
                text=OWNER_ADMIN_ROLE_BUTTON,
                callback_data=Callback.O_ROLE + "!admin",
            )
        ],
        [
            InlineKeyboardButton(
                text=OWNER_MENU_BUTTON,
                callback_data=Callback.OWNER_MENU,
            )
        ],
    ]
)

o_employees_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=OWNER_EMPLOYEES_MODERATORS_BUTTON,
                callback_data=Callback.O_CHOOSE_EMPLOYEES + "!moderator",
            )
        ],
        [
            InlineKeyboardButton(
                text=OWNER_EMPLOYEES_ADMINS_BUTTON,
                callback_data=Callback.O_CHOOSE_EMPLOYEES + "!admin",
            )
        ],
        [
            InlineKeyboardButton(
                text=OWNER_MENU_BUTTON,
                callback_data=Callback.OWNER_MENU,
            )
        ],
    ]
)


def get_employees_kb(employees, role, page, max_page):
    inline_keyboard = []

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=APPEAL_PREV,
                callback_data=f"{Callback.O_PREV_PAGE}!{role}!{page-1}",
            ),
            InlineKeyboardButton(
                text=PAGE_INDICATOR.format(current=page + 1, total=max_page + 1),
                callback_data=Callback.EMPTY,
            ),
            InlineKeyboardButton(
                text=APPEAL_NEXT,
                callback_data=f"{Callback.O_NEXT_PAGE}!{role}!{page+1}",
            ),
        ]
    )

    row = []
    for employer in employees:
        row.append(
            InlineKeyboardButton(
                text=f"{'@' + employer['username'] if employer['username'] else employer['tg_id']}",
                callback_data=f"{Callback.O_EMPLOYER_INFO}!{role}!{employer['tg_id']}",
            )
        )

        if len(row) == 2:
            inline_keyboard.append(row)
            row = []

    if row:
        inline_keyboard.append(row)

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=OWNER_EMPLOYEE_MANAGER_BUTTON,
                callback_data=Callback.O_MANAGE_EMPLOYEES,
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_employer_manager_kb(user_id: int, role: str, is_banned: bool):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=OWNER_REMOVE_ROLE_BUTTON,
                callback_data=f"{Callback.O_REMOVE_ROLE}!{role}!{user_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text=OWNER_UNBAN_BUTTON if is_banned else OWNER_BAN_BUTTON,
                callback_data=f"{Callback.O_BAN_STATE}!{'unban' if is_banned else 'ban'}!{user_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text=OWNER_MENU_BUTTON,
                callback_data=Callback.OWNER_MENU,
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_appeals_kb(user_id: int, page: int, max_page: int):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=APPEAL_PREV,
                callback_data=f"{Callback.O_PREV_PAGE}!{page-1}",
            ),
            InlineKeyboardButton(
                text=PAGE_INDICATOR.format(current=page + 1, total=max_page + 1),
                callback_data=Callback.EMPTY,
            ),
            InlineKeyboardButton(
                text=APPEAL_NEXT,
                callback_data=f"{Callback.O_NEXT_PAGE}!{page+1}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=OWNER_BAN_AUTHOR_BUTTON,
                callback_data=f"{Callback.O_BAN_USER}!{user_id}",
            )
        ],
        [
            InlineKeyboardButton(
                text=OWNER_MENU_BUTTON,
                callback_data=Callback.OWNER_MENU,
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_bans_kb(users, page: int, max_page: int):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=APPEAL_PREV,
                callback_data=f"{Callback.O_PREV_PAGE}!{page-1}",
            ),
            InlineKeyboardButton(
                text=PAGE_INDICATOR.format(current=page + 1, total=max_page + 1),
                callback_data=Callback.EMPTY,
            ),
            InlineKeyboardButton(
                text=APPEAL_NEXT,
                callback_data=f"{Callback.O_NEXT_PAGE}!{page+1}",
            ),
        ]
    ]

    row = []
    for user in users:
        row.append(
            InlineKeyboardButton(
                text=f"{'@' + user['username'] if user['username'] else user['tg_id']}",
                callback_data=f"{Callback.O_USER_INFO}!{user['tg_id']}",
            )
        )

        if len(row) == 2:
            inline_keyboard.append(row)
            row = []

    if row:
        inline_keyboard.append(row)

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text=OWNER_MENU_BUTTON,
                callback_data=Callback.OWNER_MENU,
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def get_ban_history_kb(user_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=OWNER_UNBAN_BUTTON,
                    callback_data=f"{Callback.O_UNBAN_USER}!{user_id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=OWNER_MENU_BUTTON,
                    callback_data=Callback.OWNER_MENU,
                )
            ],
        ]
    )
