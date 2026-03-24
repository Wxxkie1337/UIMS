from aiogram import F
from aiogram.types import CallbackQuery

from config import BOT_USER
from keyboards.global_kb import Callback, g_main_menu_kb
from keyboards.owner_kb import o_roles_kb, o_ownermenu_kb
from utils.messages import (
    OWNER_CHOOSE_ROLE_TEXT,
    OWNER_ROLE_LINK_ERROR_TEXT,
    OWNER_ROLE_LINK_TEXT,
)
from utils.telegram import (
    update_last_message,
    UIContext
)

from .shared import database, router


@router.callback_query(F.data == Callback.O_GENERATE_ROLE_URL)
async def choose_role_menu(callback: CallbackQuery):
    await callback.answer()
    
    ctx = await UIContext.from_callback(callback, database)

    msg = await ctx.update_message(
        text=OWNER_CHOOSE_ROLE_TEXT,
        reply_markup=o_roles_kb,
    )
    await update_last_message(ctx.db, ctx.user_id, msg)


@router.callback_query(F.data.startswith(Callback.O_ROLE))
async def generate_role_url(callback: CallbackQuery):
    await callback.answer()

    role = callback.data.split("!")[1]
    token = await database.create_invite(role)

    if not token:
        await callback.answer(
            text=OWNER_ROLE_LINK_ERROR_TEXT,
            show_alert=True,
        )
        return

    ctx = await UIContext.from_callback(callback, database)

    msg = await ctx.update_message(
        text=OWNER_ROLE_LINK_TEXT.format(bot_user=BOT_USER, token=token),
        reply_markup=o_ownermenu_kb,
    )
    
    await update_last_message(ctx.db, ctx.user_id, msg)
