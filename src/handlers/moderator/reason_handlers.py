import html

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.common import delete_message
from keyboards.global_kb import Callback, g_view_appeals_kb
from keyboards.moderator_kb import m_confirm_reason_kb
from utils import get_chat_id

from .common import ModeratorStates, database, router
from .menu_handlers import check_appeals


@router.callback_query(F.data == Callback.M_REJECT_APPEAL)
async def reject_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    write_reason = await callback.message.answer(
        "<b>Отклонение обращения</b>\n\n"
        "Укажите причину отклонения. Этот текст увидит пользователь."
    )

    await state.update_data(m_write_reason_id=write_reason.message_id)
    await state.set_state(ModeratorStates.input_reason)


@router.message(ModeratorStates.input_reason)
async def get_reason(message: Message, state: FSMContext):
    msg = message.text
    await message.delete()
    await state.update_data(reason_msg=msg)

    wait_confirm_msg = await message.answer(
        text=(
            "<b>Подтверждение отклонения</b>\n\n"
            "Проверьте причину ниже и подтвердите действие:\n\n"
            f"<code>{html.escape(msg)}</code>"
        ),
        reply_markup=m_confirm_reason_kb,
    )
    await state.update_data(
        reason_msg=message.text, m_wait_reason_id=wait_confirm_msg.message_id
    )


@router.callback_query(ModeratorStates.input_reason, F.data == Callback.M_ACCEPT_REASON)
async def accept_reason(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_message(
        callback.message.bot,
        get_chat_id(callback),
        await state.get_value("last_bot_message_id"),
    )
    await delete_message(
        callback.message.bot,
        get_chat_id(callback),
        await state.get_value("m_write_reason_id"),
    )
    await delete_message(
        callback.message.bot,
        get_chat_id(callback),
        await state.get_value("m_wait_reason_id"),
    )

    reason_msg = await state.get_value("reason_msg")
    last_appeal_id = await state.get_value("m_last_appeal_id")
    appeal_creator_appeal = await database.get_user_id_by_appeal(
        appeal_id=last_appeal_id
    )

    msg = await callback.message.bot.send_message(
        chat_id=appeal_creator_appeal,
        text="Одно из ваших обращений было проверено модераторами.",
        reply_markup=g_view_appeals_kb,
    )

    await state.update_data(last_bot_message_id=msg.message_id)
    await database.set_reject_reason(last_appeal_id, reason_msg)
    await database.reject_appeal(last_appeal_id)

    page = 0
    if p := await state.get_value("m_page"):
        page = max(0, p - 1)

    await check_appeals(callback, state, start_page=page)
