from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.global_kb import Callback
from keyboards.owner_kb import get_ban_history_kb, get_bans_kb, o_ownermenu_kb
from utils.messages import (
    OWNER_BAN_HISTORY_EMPTY_TEXT,
    OWNER_BAN_HISTORY_TITLE_TEXT,
    OWNER_BAN_HISTORY_USER_CARD_TEXT,
    OWNER_NOTIFY_UNBANNED_TEXT,
    OWNER_ROLE_ADMIN_TEXT,
    OWNER_ROLE_MODERATOR_TEXT,
    OWNER_ROLE_USER_TEXT,
)
from utils.misc import format_datetime, get_user_link
from utils.telegram import (
    notify,
    update_last_message,
    UIContext
)

from .shared import OwnerStates, database, router

USERS_COUNT = 4


async def show_banned_users(callback, page):
    if page < 0:
        return
    
    ctx = await UIContext.from_callback(callback, database)

    offset = page * USERS_COUNT

    users = await database.get_banned_users(offset, USERS_COUNT)
    users_count = await database.get_banned_users_count()

    if users_count == 0:
        msg = await ctx.update_message(
            text=OWNER_BAN_HISTORY_EMPTY_TEXT,
            reply_markup=o_ownermenu_kb
        )
        await update_last_message(database, ctx.user_id, msg)
        return

    max_page = max(0, (users_count - 1) // USERS_COUNT)

    if page > max_page:
        return

    msg = await ctx.update_message(
        text=OWNER_BAN_HISTORY_TITLE_TEXT,
        reply_markup=get_bans_kb(users, page, max_page)
    )
    
    await update_last_message(database, ctx.user_id, msg)


@router.callback_query(F.data == Callback.O_BAN_HISTORY)
async def ban_history(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(OwnerStates.bans_history)
    await show_banned_users(callback, 0)


@router.callback_query(
    OwnerStates.bans_history,
    F.data.startswith(Callback.O_PREV_PAGE) | F.data.startswith(Callback.O_NEXT_PAGE),
)
async def page_handler(callback: CallbackQuery):
    await callback.answer()
    _, page = callback.data.split("!")
    await show_banned_users(callback, int(page))


@router.callback_query(OwnerStates.bans_history, F.data.startswith(Callback.O_USER_INFO))
async def banned_user_info(callback: CallbackQuery):
    await callback.answer()
    _, tg_id = callback.data.split("!")
    
    ctx = await UIContext.from_callback(callback, database)

    user_data = await database.get_user_data(int(tg_id))
    username = user_data.get("username")

    is_admin = await database.is_admin(int(tg_id))
    is_moderator = await database.is_moderator(int(tg_id))

    if is_admin:
        role = OWNER_ROLE_ADMIN_TEXT
    elif is_moderator:
        role = OWNER_ROLE_MODERATOR_TEXT
    else:
        role = OWNER_ROLE_USER_TEXT

    msg = await ctx.update_message(
        text=OWNER_BAN_HISTORY_USER_CARD_TEXT.format(
            userlink=get_user_link(int(tg_id), username),
            username=username,
            role=role,
            created_at=format_datetime(user_data.get("created_at")),
        ),
        disable_web_page_preview=True,
        reply_markup=get_ban_history_kb(int(tg_id))
    )
    
    await update_last_message(database, ctx.user_id, msg)


@router.callback_query(OwnerStates.bans_history, F.data.startswith(Callback.O_UNBAN_USER))
async def unban_user(callback: CallbackQuery):
    await callback.answer()
    _, tg_id = callback.data.split("!")
    await database.unban_user(int(tg_id))
    await notify(callback.message.bot, int(tg_id), OWNER_NOTIFY_UNBANNED_TEXT)
    await show_banned_users(callback, 0)
