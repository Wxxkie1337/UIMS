from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.global_kb import Callback
from keyboards.admin_kb import a_menu_kb
from utils.telegram import (
    update_last_message,
    UIContext
)
from utils.messages import ADMIN_MENU_TEXT

from .shared import router, database


@router.callback_query(F.data == Callback.ADMIN_MENU)
async def admin_menu(callback: CallbackQuery):
    await callback.answer()
    
    ctx = await UIContext.from_callback(callback, database)

    msg = await ctx.update_message(
        text=ADMIN_MENU_TEXT,
        reply_markup=a_menu_kb
    )
    
    await update_last_message(database, ctx.user_id, msg)