from typing import Optional

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.global_kb import Callback
from keyboards.owner_kb import o_employees_kb, get_employees_kb, get_employer_manager_kb
from utils.messages import (
    OWNER_ADMINS_LIST_TEXT,
    OWNER_EMPLOYEES_MENU_TEXT,
    OWNER_EMPLOYEE_BANNED_TEXT,
    OWNER_EMPLOYEE_CARD_TEXT,
    OWNER_EMPLOYEE_NOT_FOUND_TEXT,
    OWNER_EMPLOYEE_USERNAME_MISSING,
    OWNER_MODERATORS_LIST_TEXT,
    OWNER_MODERATOR_STATS_TEXT,
    OWNER_NOTIFY_ADMIN_REMOVED_TEXT,
    OWNER_NOTIFY_BANNED_TEXT,
    OWNER_NOTIFY_MODERATOR_REMOVED_TEXT,
    OWNER_NOTIFY_UNBANNED_TEXT,
    OWNER_ROLE_ADMIN_TEXT,
    OWNER_ROLE_MODERATOR_TEXT,
)
from utils.telegram import (
    update_last_message,
    notify,
    UIContext
)
from utils.misc import format_datetime, get_user_link

from .shared import database, router, OwnerStates

EMPLOYEES_COUNT = 2


async def get_role_data(role: str, offset: int) -> Optional[tuple]:
    if role == "admin":
        text = OWNER_ADMINS_LIST_TEXT
        total = await database.get_admins_count()
        employees = await database.get_admins(offset, EMPLOYEES_COUNT)
    elif role == "moderator":
        text = OWNER_MODERATORS_LIST_TEXT
        total = await database.get_moderators_count()
        employees = await database.get_moderators(offset, EMPLOYEES_COUNT)
    else:
        return None
    return text, total, employees


async def show_employees_message(callback: CallbackQuery, role: str, page: int):
    if page < 0:
        return
    
    ctx = await UIContext.from_callback(callback, database)

    offset = page * EMPLOYEES_COUNT
    role_data = await get_role_data(role, offset)
    if not role_data:
        return
    
    text, total, employees = role_data
    max_page = max(0, (total - 1) // EMPLOYEES_COUNT)
    
    if page > max_page:
        return

    msg = await ctx.update_message(
        text=text,
        reply_markup=get_employees_kb(
            employees=employees,
            role=role,
            page=page,
            max_page=max_page
        )
    )
    await update_last_message(ctx.db, ctx.user_id, msg)


@router.callback_query(F.data == Callback.O_MANAGE_EMPLOYEES)
async def manage_employees_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await state.set_state(OwnerStates.manage_employees)
    
    ctx = await UIContext.from_callback(callback, database)
    
    msg = await ctx.update_message(
        text=OWNER_EMPLOYEES_MENU_TEXT,
        reply_markup=o_employees_kb
    )
    
    await update_last_message(ctx.db, ctx.user_id, msg)


@router.callback_query(OwnerStates.manage_employees, F.data.startswith(Callback.O_CHOOSE_EMPLOYEES))
async def choose_employees(callback: CallbackQuery):
    await callback.answer()
    _, role = callback.data.split("!")
    await show_employees_message(callback, role, 0)


@router.callback_query(OwnerStates.manage_employees, F.data.startswith(Callback.O_NEXT_PAGE) | F.data.startswith(Callback.O_PREV_PAGE))
async def page_handler(callback: CallbackQuery):
    await callback.answer()
    _, role, page = callback.data.split("!")
    await show_employees_message(callback, role, int(page))


@router.callback_query(OwnerStates.manage_employees, F.data.startswith(Callback.O_EMPLOYER_INFO))
async def employer_info(callback: CallbackQuery):
    await callback.answer()
    
    _, role, target_id = callback.data.split("!")
    target_id = int(target_id)
    
    ctx = await UIContext.from_callback(callback, database)

    role_block = OWNER_ROLE_MODERATOR_TEXT if role == "moderator" else OWNER_ROLE_ADMIN_TEXT

    if role == "moderator":
        data = await database.get_moderator_data(target_id)
    else:
        data = await database.get_admin_data(target_id)

    if not data:
        await callback.answer(OWNER_EMPLOYEE_NOT_FOUND_TEXT, show_alert=True)
        return

    username = data.get("username")
    created_at = format_datetime(data.get("created_at"))
    userlink = get_user_link(target_id, username)
    is_banned = data.get("is_banned", False)
    ban_notice = OWNER_EMPLOYEE_BANNED_TEXT if is_banned else ""
    stats_block = ""

    if role == "moderator":
        stats_block = OWNER_MODERATOR_STATS_TEXT.format(
            accepted=data["accepted_appeals"],
            rejected=data["rejected_appeals"],
        )

    text = OWNER_EMPLOYEE_CARD_TEXT.format(
        ban_notice=ban_notice,
        userlink=userlink,
        username=username or OWNER_EMPLOYEE_USERNAME_MISSING,
        role=role_block,
        created_at=created_at,
        stats_block=stats_block,
    )

    msg = await ctx.update_message(
        text=text,
        reply_markup=get_employer_manager_kb(target_id, role, is_banned),
        disable_web_page_preview=True
    )
    await update_last_message(ctx.db, ctx.user_id, msg)
    

@router.callback_query(OwnerStates.manage_employees, F.data.startswith(Callback.O_REMOVE_ROLE))
async def remove_role(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    _, role, tg_id = callback.data.split("!")
    
    if role == "moderator":
        await notify(callback.message.bot, int(tg_id), OWNER_NOTIFY_MODERATOR_REMOVED_TEXT)
        await database.remove_moderator(int(tg_id))
    elif role == "admin":
        await notify(callback.message.bot, int(tg_id), OWNER_NOTIFY_ADMIN_REMOVED_TEXT)
        await database.remove_admin(int(tg_id))
        
    await manage_employees_menu(callback, state)
    

@router.callback_query(OwnerStates.manage_employees, F.data.startswith(Callback.O_BAN_STATE))
async def set_ban_state_user(callback: CallbackQuery, state: FSMContext):
    _, ban_state, tg_id = callback.data.split("!")
    
    if ban_state == "unban":
        await notify(callback.message.bot, int(tg_id), OWNER_NOTIFY_UNBANNED_TEXT)
        await database.unban_user(int(tg_id))
    elif ban_state == "ban":
        await notify(callback.message.bot, int(tg_id), OWNER_NOTIFY_BANNED_TEXT)
        await database.ban_user(int(tg_id))
        
    await manage_employees_menu(callback, state)
