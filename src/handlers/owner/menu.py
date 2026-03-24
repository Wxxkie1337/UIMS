from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.global_kb import Callback
from keyboards.owner_kb import o_menu_kb
from utils.messages import OWNER_MENU_TEXT
from utils.telegram import (
    update_last_message,
    UIContext
)

from .shared import database, router


@router.callback_query(F.data == Callback.OWNER_MENU)
async def owner_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(None)
    
    ctx = await UIContext.from_callback(callback, database)

    msg = await ctx.update_message(
        text=OWNER_MENU_TEXT,
        reply_markup=o_menu_kb,
    )
    
    await update_last_message(ctx.db, ctx.user_id, msg)
