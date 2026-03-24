from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.global_kb import Callback
from keyboards.admin_kb import a_adminmenu_kb, get_active_appeals_kb, a_cancel_kb

from utils.telegram import (
    notify,
    update_last_message,
    UIContext
)
from utils.messages import (
    ADMIN_COMPLETE_APPEAL_PROMPT_TEXT,
    ADMIN_COMPLETED_NOTIFY_TEXT,
    ADMIN_NO_ACTIVE_APPEALS_TEXT,
    ADMIN_RETURNED_TO_APPROVED_NOTIFY_TEXT,
    ADMIN_RETURN_TO_APPROVED_FAILED_TEXT,
    ADMIN_RETURN_TO_DEFERRED_FAILED_TEXT,
    LABEL_APPEAL_NUMBER,
)

from .shared import router, database, AdminStates, get_formatted_text


async def show_appeal_message(callback, page):
    ctx = await UIContext.from_callback(callback, database)

    max_page = await database.get_active_appeals_count(ctx.user_id) - 1

    if max_page < 0:
        msg = await ctx.update_message(
            text=ADMIN_NO_ACTIVE_APPEALS_TEXT,
            reply_markup=a_adminmenu_kb
        )
        await update_last_message(ctx.db, ctx.user_id, msg)
        return

    if page > max_page or page < 0:
        return

    appeals = await database.get_active_appeals(ctx.user_id, page, 1)
    if not appeals:
        return

    appeal = appeals[0]
    appeal_id = appeal.get("id")

    kb = get_active_appeals_kb(page, max_page, appeal_id)

    msg = await ctx.update_message(**get_formatted_text(appeal, kb))

    await update_last_message(database, ctx.user_id, msg)


@router.callback_query(F.data == Callback.A_CHECK_ACTIVE_APPEALS)
async def check_active_appeals(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminStates.check_active_appeals)
    await show_appeal_message(callback, 0)


@router.callback_query(AdminStates.check_active_appeals, F.data.startswith(Callback.A_PAGE))
async def page_handler(callback: CallbackQuery):
    await callback.answer()
    _, page = callback.data.split("!")
    await show_appeal_message(callback, int(page))


@router.callback_query(AdminStates.check_active_appeals, F.data.startswith(Callback.A_COMPLETE_APPEAL))
async def complete_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    _, appeal_id = callback.data.split("!")
    
    msg = await callback.message.answer(
        text=ADMIN_COMPLETE_APPEAL_PROMPT_TEXT,
        reply_markup=a_cancel_kb
    )
    
    await state.update_data(msg_id=msg.message_id, appeal_id=int(appeal_id))
    await state.set_state(AdminStates.complete_message)
    
    
@router.callback_query(AdminStates.check_active_appeals, F.data.startswith(Callback.A_BACK_TO_ACTIVE))
async def back_to_active(callback: CallbackQuery):
    await callback.answer()
    _, appeal_id = callback.data.split("!")
    
    ctx = await UIContext.from_callback(callback, database)
    
    appealer_id = await ctx.db.get_user_id_by_appeal(int(appeal_id))
    if appealer_id and await ctx.db.set_appeal_status(int(appeal_id), "accepted"):
        await notify(ctx.bot, appealer_id,
            text=ADMIN_RETURNED_TO_APPROVED_NOTIFY_TEXT
        )
    else:
        await notify(ctx.bot, ctx.chat_id,
            text=ADMIN_RETURN_TO_APPROVED_FAILED_TEXT
        )
    await show_appeal_message(callback, 0)
    
    
@router.callback_query(AdminStates.check_active_appeals, F.data.startswith(Callback.A_BACK_TO_DEFERRED))
async def back_to_deferred(callback: CallbackQuery):
    await callback.answer()
    _, appeal_id = callback.data.split("!")
    
    ctx = await UIContext.from_callback(callback, database)

    if not (await ctx.db.set_appeal_status(int(appeal_id), "deferred", deferred_by=ctx.user_id)):
        await notify(ctx.bot, ctx.chat_id,
            text=ADMIN_RETURN_TO_DEFERRED_FAILED_TEXT
        )
    await show_appeal_message(callback, 0)
