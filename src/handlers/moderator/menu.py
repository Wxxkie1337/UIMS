from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.global_kb import Callback
from keyboards.moderator_kb import m_menu_kb
from utils.telegram import (
    update_last_message,
    UIContext
)
from utils.messages import MODERATOR_MENU_TEXT

from .shared import ModeratorStates, database, router, switch_appeals


@router.callback_query(F.data == Callback.MODERATOR_MENU)
async def handle_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    ctx = await UIContext.from_callback(callback, database)
    
    await state.set_state(ModeratorStates.moderator_view)
    
    msg = await ctx.update_message(
        text=MODERATOR_MENU_TEXT,
        reply_markup=m_menu_kb,
    )
    
    await update_last_message(ctx.db, ctx.user_id, msg)


@router.callback_query(F.data == Callback.M_CHECK_APPEALS)
async def check_appeals(callback: CallbackQuery, state: FSMContext, *, start_page=0):
    await state.update_data(m_page=start_page)
    await callback.answer()
    await switch_appeals(callback, state, start_page)
