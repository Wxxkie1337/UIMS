from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.global_kb import Callback
from keyboards.owner_kb import o_ownermenu_kb
from utils.messages import OWNER_APPEALS_HISTORY_EMPTY_TEXT, OWNER_NOTIFY_BANNED_TEXT
from utils.telegram import (
    notify,
    update_last_message,
    UIContext
)

from .shared import OwnerStates, database, get_formatted_text, router


async def show_appeals_message(callback: CallbackQuery, page: int):  
    max_page = await database.get_rejected_appeals_count() - 1
    
    ctx = await UIContext.from_callback(callback, database)

    data = await get_formatted_text(page, max_page)
    if data is None:
        msg = await ctx.update_message(
            text=OWNER_APPEALS_HISTORY_EMPTY_TEXT,
            reply_markup=o_ownermenu_kb,
        )
        
        await update_last_message(database, ctx.user_id, msg)
        return

    msg = await ctx.update_message(**data)

    await update_last_message(database, ctx.user_id, msg)


@router.callback_query(F.data == Callback.O_APPEALS_HISTORY)
async def appeals_history(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(OwnerStates.appeals_history)
    await show_appeals_message(callback, 0)


@router.callback_query(
    OwnerStates.appeals_history,
    F.data.startswith(Callback.O_NEXT_PAGE) | F.data.startswith(Callback.O_PREV_PAGE),
)
async def page_handler(callback: CallbackQuery):
    await callback.answer()
    _, page = callback.data.split("!")
    await show_appeals_message(callback, int(page))


@router.callback_query(OwnerStates.appeals_history, F.data.startswith(Callback.O_BAN_USER))
async def ban_user(callback: CallbackQuery):
    await callback.answer()
    _, tg_id = callback.data.split("!")
    await notify(callback.message.bot, int(tg_id), OWNER_NOTIFY_BANNED_TEXT)
    await database.ban_user(int(tg_id))
    await show_appeals_message(callback, 0)
