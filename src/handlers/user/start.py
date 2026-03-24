from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import OWNERS_ID
from db import DataBase
from keyboards.global_kb import Callback, get_start_kb
from utils.messages import INVALID_INVITE_TEXT, USER_MAIN_MENU_TEXT, WELCOME_TEXT
from utils.telegram import (
    notify,
    update_last_message,
    UIContext
)

router = Router()
database = DataBase()


@router.message(Command("start", "new"))
async def handle_start_command(message: Message, command: CommandObject, state: FSMContext):
    await state.set_state(None)
    
    ctx = await UIContext.from_message(message, database)

    await database.add_user(ctx.user_id, ctx.username)

    args = command.args
    if args and args.startswith("invite_"):
        token = args.split("invite_", 1)[1]
        role = await database.use_role(token)

        if role == "moderator":
            await database.make_moderator(ctx.user_id)
        elif role == "admin":
            await database.make_admin(ctx.user_id)

        if role is None:
            await notify(message.bot, ctx.chat_id, INVALID_INVITE_TEXT)

    is_owner = ctx.user_id in OWNERS_ID

    if is_owner:
        await database.make_admin(ctx.user_id)
        await database.make_moderator(ctx.user_id)

    is_moderator = await database.is_moderator(ctx.user_id)
    is_admin = await database.is_admin(ctx.user_id)

    msg = await ctx.send_new(
        text=WELCOME_TEXT,
        reply_markup=get_start_kb(
            is_moderator=is_moderator,
            is_admin=is_admin,
            is_owner=is_owner,
        )
    )

    await update_last_message(database, ctx.user_id, msg)


@router.callback_query(F.data == Callback.MAIN_MENU)
async def handle_main_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(None)
    
    ctx = await UIContext.from_callback(callback, database)

    is_moderator = await database.is_moderator(ctx.user_id)
    is_admin = await database.is_admin(ctx.user_id)
    is_owner = ctx.user_id in OWNERS_ID

    msg = await ctx.update_message(
        text=USER_MAIN_MENU_TEXT,
        reply_markup=get_start_kb(
            is_moderator=is_moderator,
            is_admin=is_admin,
            is_owner=is_owner,
        )
    )
    await update_last_message(ctx.db, ctx.user_id, msg)


@router.callback_query(F.data.startswith(Callback.UNDERSTAND))
async def delete_understand_msg(callback: CallbackQuery):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass


@router.callback_query(F.data == Callback.EMPTY)
async def handle_empty(callback: CallbackQuery):
    await callback.answer()
