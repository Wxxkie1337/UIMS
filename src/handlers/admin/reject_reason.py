import html

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.global_kb import Callback
from keyboards.admin_kb import get_reason_kb
from utils.telegram import (
    notify,
    UIContext
)
from utils.messages import (
    ADMIN_REASON_SENT_TEXT,
    ADMIN_REJECT_CONFIRM_TEXT,
    ADMIN_REJECT_FAILED_TEXT,
    ADMIN_REJECT_PROMPT_TEXT,
    ADMIN_REJECTED_NOTIFY_TEXT,
    LABEL_APPEAL_NUMBER,
)

from .shared import router, database, AdminStates


@router.callback_query(F.data.startswith(Callback.A_REJECT_APPEAL))
async def reject_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    await state.set_state(AdminStates.wait_reason)
    _, appeal_id = callback.data.split("!")
    
    msg = await callback.message.answer(ADMIN_REJECT_PROMPT_TEXT)
    await state.update_data(
        a_message_id=msg.message_id,
        a_appeal_id=appeal_id
    )
    
    
@router.message(AdminStates.wait_reason, F.text)
async def reason_handler(message: Message, state: FSMContext):
    await state.set_state(AdminStates.reject_reason)
    
    appeal_id = await state.get_value("a_appeal_id")
    
    ctx = await UIContext.from_message(message, database)
    
    last_message_id = await state.get_value("a_message_id")
    text = html.escape(message.text)

    msg = await ctx.update_specific(
        message_id=last_message_id,
        text=ADMIN_REJECT_CONFIRM_TEXT.format(
            reason=f"<code>{text}</code>"
        ),
        reply_markup=get_reason_kb(1, int(appeal_id))
    )
    
    if msg:
        await state.update_data(a_message_id=msg)
    await state.update_data(a_reason_message=text)

    
@router.callback_query(AdminStates.reject_reason, F.data.startswith(Callback.A_ACCEPT_REASON))
async def accept_reason(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    _, appeal_id = callback.data.split("!")
    appeal = await database.get_appeal_by_id(int(appeal_id))
    
    ctx = await UIContext.from_callback(callback, database)
    
    last_message_id = await state.get_value("a_message_id")
    
    if await database.reject_appeal(int(appeal_id), await state.get_value("a_reason_message")):
        await notify(
            bot=ctx.bot,
            chat_id=appeal.get("user_id"), 
            text=ADMIN_REJECTED_NOTIFY_TEXT.format(
                appeal_number=f"{LABEL_APPEAL_NUMBER} {appeal_id}"
            ),
        )

        await ctx.update_specific(
            message_id=last_message_id,
            text=ADMIN_REASON_SENT_TEXT,
            reply_markup=get_reason_kb(2, int(appeal_id))
        )
    else:
        await ctx.update_specific(
            message_id=last_message_id,
            text=ADMIN_REJECT_FAILED_TEXT,
            reply_markup=get_reason_kb(2, int(appeal_id))
        )


@router.callback_query(F.data.startswith(Callback.A_BACK_TO_APPEALS))
async def back_to_appeals(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.set_state(None)
