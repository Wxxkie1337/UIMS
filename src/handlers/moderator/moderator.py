"""

!!!!!!!!!!!!!!!!!!!!!!
сделать свап обращений
!!!!!!!!!!!!!!!!!!!!!!

"""


from html import escape

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from db import DataBase
from handlers.common import answer, delete_message
from keyboards.global_kb import Callback, g_main_menu_kb
from keyboards.moderator_kb import m_menu_kb, m_confirm_reason_kb, get_unmoderated_appeal_kb
from utils import get_chat_id, get_user_id


router = Router()
database = DataBase()


class ModeratorStates(StatesGroup):
    moderator_view = State()
    input_reason = State()


def _escape_html_text(text: str) -> str:
    return escape(text)

async def get_formatted_text(offset: int, state: FSMContext):
    appeals = await database.get_unmoderated_appeals(
        limit=1,
        offset=offset,
    )

    if not appeals:
        return None

    appeal = appeals[0]
    total = await database.get_appeals_count(is_accepted=False, is_rejected=False)

    await state.update_data(m_last_appeal_id=appeal.get("id"))

    return {
        "photo": appeal["photo_id"],
        "caption": (
            f"📅 <b>Дата:</b> {appeal['created_at']}\n"
            f"🗂 <b>Категория:</b> {appeal['category']}\n"
            f"📝 <b>Описание:</b> {appeal['message']}"
        ),
        "reply_markup": get_unmoderated_appeal_kb(offset + 1, total, appeal['latitude'], appeal['longitude']),
        "parse_mode": "HTML",
    }
    
    
async def switch_appeals(callback: CallbackQuery, state: FSMContext, page: int):
    await delete_message(
        callback.message.bot, get_chat_id(callback), await state.get_value("last_bot_message_id")
    )

    data = await get_formatted_text(page, state)
    if not data:
        await answer(
            text="<b>Обращения не найдены.</b>\nВыберите действие:",
            message=callback.message,
            state=state,
            reply_markup=m_menu_kb
        )
        return
    
    msg = await callback.message.answer_photo(**data)
    await state.update_data(
        last_bot_message_id=msg.message_id,
        m_page=page
    )
    

@router.callback_query(F.data == Callback.MODERATOR_MENU)
async def handle_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user_id = get_user_id(callback)
    chat_id = get_chat_id(callback)
    callback_message_id = callback.message.message_id if callback.message else None
    last_bot_message_id = await state.get_value("last_bot_message_id")
    
    await state.set_state(ModeratorStates.moderator_view)

    # Удаляем сообщение с кнопкой меню и последнее сообщение бота.
    # Если это одно и то же сообщение, удаляем только один раз.
    await delete_message(callback.bot, chat_id, callback_message_id)
    if last_bot_message_id != callback_message_id:
        await delete_message(callback.bot, chat_id, last_bot_message_id)

    if callback_message_id or last_bot_message_id:
        await state.update_data(last_bot_message_id=None)

    if not await database.is_moderator(user_id):
        await answer(
            text="<b>Недостаточно прав</b> для использования этой команды.",
            message=callback.message,
            state=state,
            reply_markup=g_main_menu_kb,
        )
        return

    await answer(
        text="<b>Выберите действие:</b>",
        message=callback.message,
        state=state,
        reply_markup=m_menu_kb
    )
    

@router.callback_query(F.data == Callback.M_CHECK_APPEALS)
async def check_appeals(callback: CallbackQuery, state: FSMContext):
    await state.update_data(m_page=0)
    await callback.answer()
    await switch_appeals(callback, state, 0)


@router.callback_query(F.data == Callback.M_REJECT_APPEAL)
async def reject_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    appeal_id       = await state.get_value("m_last_appeal_id", None)
    user_appeal_id  = await database.get_user_id_by_appeal(appeal_id)
    
    if appeal_id is None or not user_appeal_id:
        return
    
    #await database.reject_appeal(appeal_id)
    
    write_reason = await callback.message.answer("<b>Введите причину отказа:</b>")
    
    await state.update_data(m_write_reason_id=write_reason.message_id)
    await state.set_state(ModeratorStates.input_reason)
    #await state.update_data(m_last_appeal_id=None)
    #await check_appeals(callback, state)
    
    
@router.message(ModeratorStates.input_reason)
async def get_reason(message: Message, state: FSMContext):
    msg = message.text
    await message.delete()
    await state.update_data(reason_msg=msg)
    
    escaped_reason = _escape_html_text(msg)
    wait_confirm_msg = await message.answer(
        text=(
            "<b>Подтвердите отклонение обращения с подписью:</b>\n"
            f"<pre>{escaped_reason}</pre>"
        ),
        reply_markup=m_confirm_reason_kb,
    )
    await state.update_data(m_wait_reason_id=wait_confirm_msg.message_id)
    

@router.callback_query(ModeratorStates.input_reason, F.data == Callback.M_ACCEPT_REASON)
async def accept_reason(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await delete_message(
        callback.message.bot, get_chat_id(callback), await state.get_value("last_bot_message_id")
    )
    await delete_message(
        callback.message.bot, get_chat_id(callback), await state.get_value("m_write_reason_id")
    )
    await delete_message(
        callback.message.bot, get_chat_id(callback), await state.get_value("m_wait_reason_id")
    )
    
    await handle_menu(callback, state)
    
    
@router.callback_query(F.data == Callback.M_ACCEPT_APPEAL)
async def accept_appeal(callback: CallbackQuery, state: FSMContext):
    appeal_id = await state.get_value("m_last_appeal_id", None)
    if appeal_id is None:
        return
    await database.accept_appeal(appeal_id)
    await state.update_data(m_last_appeal_id=None)
    await check_appeals(callback, state)
    
    
@router.callback_query(F.data == Callback.M_APPEAL_NEXT)
async def next_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    page = await state.get_value("m_page")
    next_page = page + 1
    max_page = await database.get_appeals_count(is_accepted=False, is_rejected=False) - 1

    if next_page > max_page or page == max_page:
        return
    
    await switch_appeals(callback, state, next_page)
    
    
@router.callback_query(F.data == Callback.M_APPEAL_PREV)
async def next_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    page = await state.get_value("m_page")
    next_page = page - 1
    max_page = await database.get_appeals_count(is_accepted=False, is_rejected=False) - 1

    if next_page < 0 or page == 0:
        return
    
    await switch_appeals(callback, state, next_page)
