from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.global_kb import Callback
from keyboards.admin_kb import a_adminmenu_kb, get_new_appeals_kb

from utils.telegram import (
    notify, 
    update_last_message,
    UIContext
)
from utils.messages import (
    ADMIN_TO_WORK_NOTIFY_TEXT, 
    LABEL_APPEAL_NUMBER,
    ADMIN_NO_APPEALS_TEXT
)

from .shared import router, database, AdminStates, get_formatted_text


async def show_appeal_message(callback, page):
    ctx = await UIContext.from_callback(callback, database)

    max_page = await database.get_moderated_appeals_count()
     
    if max_page == 0:
        msg = await ctx.update_message(
            text=ADMIN_NO_APPEALS_TEXT,
            reply_markup=a_adminmenu_kb
        )
        
        await update_last_message(ctx.db, ctx.user_id, msg)
        return
    
    max_page -= 1
    if page < 0 or page > max_page:
        return

    appeals = await database.get_moderated_appeals(page, 1)
    if not appeals:
        return
    
    appeal = appeals[0]
    appeal_id = appeal.get("id")
    
    kb = get_new_appeals_kb(page, max_page, appeal_id)
    data = get_formatted_text(appeal, kb)
    
    msg = await ctx.update_message(**data)

    await update_last_message(ctx.db, ctx.user_id, msg)


@router.callback_query(F.data == Callback.A_CHECK_MODERATED_APPEALS)
async def check_moderated_appeals(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminStates.check_moderated_appeals)
    await show_appeal_message(callback, 0)
    
    
@router.callback_query(AdminStates.check_moderated_appeals, F.data.startswith(Callback.A_PAGE))
async def page_handler(callback: CallbackQuery):
    await callback.answer()
    _, page = callback.data.split("!")
    await show_appeal_message(callback, int(page))
    
    
@router.callback_query(AdminStates.check_moderated_appeals, F.data.startswith(Callback.A_DEFER_APPEAL))
async def defer_appeal(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    _, appeal_id = callback.data.split("!")
    await database.defer_appeal(user_id, int(appeal_id))
    await show_appeal_message(callback, 0)
    
    
@router.callback_query(AdminStates.check_moderated_appeals, F.data.startswith(Callback.A_TO_WORK))
async def accept_appeal(callback: CallbackQuery):
    await callback.answer()
    _, appeal_id = callback.data.split("!")
    
    ctx = await UIContext.from_callback(callback, database)
    
    appealer_id = await ctx.db.get_user_id_by_appeal(int(appeal_id))
    if appealer_id and await ctx.db.process_appeal(ctx.user_id, int(appeal_id)):
        await notify(
            ctx.bot,
            appealer_id,
            ADMIN_TO_WORK_NOTIFY_TEXT.format(
                appeal_number=f"{LABEL_APPEAL_NUMBER} {appeal_id}"
            ),
        )
    await show_appeal_message(callback, 0)
