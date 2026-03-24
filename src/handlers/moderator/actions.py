import html

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.global_kb import Callback, g_view_appeals_kb
from keyboards.moderator_kb import m_confirm_reason_kb
from utils.telegram import (
    update_last_message,
    notify,
    UIContext
)
from utils.messages import (
    MODERATOR_ACCEPTED_NOTIFY_TEXT,
    MODERATOR_REJECT_CONFIRM_TEXT,
    MODERATOR_REJECT_PROMPT_TEXT,
    MODERATOR_REJECTED_NOTIFY_TEXT,
)

from .menu import check_appeals
from .shared import ModeratorStates, database, router, switch_appeals, appeal_is_new


@router.callback_query(F.data == Callback.M_ACCEPT_APPEAL)
async def accept_appeal(callback: CallbackQuery, state: FSMContext):
    appeal_id = await state.get_value("m_last_appeal_id")
    if appeal_id is None:
        return
    
    ctx = await UIContext.from_callback(callback, database)
    
    page = 0
    if current_page := await state.get_value("m_page"):
        page = max(0, current_page - 1)
    
    if not await appeal_is_new(state):
        await check_appeals(callback, state, start_page=page)
        return

    is_accepted = await database.accept_appeal(appeal_id)
    if not is_accepted:
        await check_appeals(callback, state, start_page=page)
        return

    await database.add_accepted_count(ctx.user_id, 1)
    appeal_owner_id = await database.get_user_id_by_appeal(appeal_id=appeal_id)

    if appeal_owner_id != ctx.user_id:
        await notify(
            bot=ctx.bot,
            chat_id=appeal_owner_id,
            text=MODERATOR_ACCEPTED_NOTIFY_TEXT.format(appeal_id=appeal_id),
        )

    await check_appeals(callback, state, start_page=page)


@router.callback_query(F.data == Callback.M_APPEAL_NEXT)
async def next_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    page = await state.get_value("m_page") or 0
    next_page = page + 1
    max_page = await database.get_appeals_count() - 1

    if next_page > max_page:
        return

    await switch_appeals(callback, state, next_page)


@router.callback_query(F.data == Callback.M_APPEAL_PREV)
async def prev_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    page = await state.get_value("m_page") or 0
    prev_page = page - 1

    if prev_page < 0:
        return

    await switch_appeals(callback, state, prev_page)


@router.callback_query(F.data == Callback.M_REJECT_APPEAL)
async def reject_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    page = 0
    if current_page := await state.get_value("m_page"):
        page = max(0, current_page - 1)
    
    if not await appeal_is_new(state):
        await check_appeals(callback, state, start_page=page)
        return

    write_reason = await callback.message.answer(
        MODERATOR_REJECT_PROMPT_TEXT
    )
    await state.update_data(m_write_reason_id=write_reason.message_id)
    await state.set_state(ModeratorStates.input_reason)


@router.message(ModeratorStates.input_reason)
async def get_reason(message: Message, state: FSMContext):
    reason_text = (message.text or "").strip()
    await state.update_data(reason_msg=reason_text)

    wait_confirm_msg = await message.answer(
        text=MODERATOR_REJECT_CONFIRM_TEXT.format(
            reason=f"<code>{html.escape(reason_text)}</code>"
        ),
        reply_markup=m_confirm_reason_kb,
    )
    
    await state.set_state(ModeratorStates.wait_reason_state)
    await state.update_data(m_wait_reason_id=wait_confirm_msg.message_id)


@router.callback_query(ModeratorStates.wait_reason_state, F.data == Callback.M_ACCEPT_REASON)
async def accept_reason(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    ctx = await UIContext.from_callback(callback, database)
    
    reason_msg = await state.get_value("reason_msg")
    appeal_id = await state.get_value("m_last_appeal_id")
    appeal_owner_id = await database.get_user_id_by_appeal(appeal_id=appeal_id)

    await ctx.delete(ctx.user_id)
    await ctx.delete(await state.get_value("m_write_reason_id"))
    await ctx.delete(await state.get_value("m_wait_reason_id"))
    
    page = 0
    if current_page := await state.get_value("m_page"):
        page = max(0, current_page - 1)
    
    if not await appeal_is_new(state):
        await check_appeals(callback, state, start_page=page)
        return

    is_rejected = await database.reject_appeal(appeal_id, reason_msg)
    if not is_rejected:
        await check_appeals(callback, state, start_page=page)
        return
    
    await database.add_rejected_count(ctx.user_id, 1)

    if appeal_owner_id != ctx.user_id:
        await notify(
            bot=ctx.bot,
            chat_id=appeal_owner_id,
            text=MODERATOR_REJECTED_NOTIFY_TEXT.format(appeal_id=appeal_id)
        )
        
    await state.set_state(ModeratorStates.moderator_view)
    await check_appeals(callback, state, start_page=page)


@router.callback_query(ModeratorStates.wait_reason_state, F.data == Callback.M_CANCEL_REASON)
async def cancel_reason(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    ctx = await UIContext.from_callback(callback, database)

    await ctx.delete(await state.get_value("m_write_reason_id"))
    await ctx.delete(await state.get_value("m_wait_reason_id"))
    
    await state.update_data(
        reason_msg=None,
        m_write_reason_id=None,
        m_wait_reason_id=None,
    )
    
    await state.set_state(ModeratorStates.moderator_view)

    await switch_appeals(callback, state, await state.get_value("m_page") or 0)
