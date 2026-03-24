import html
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from db import DataBase
from keyboards.global_kb import Callback, g_main_menu_kb
from keyboards.user_kb import get_switch_kb, u_info_kb
from utils.misc import format_datetime
from utils.telegram import (
    update_last_message,
    UIContext
)
from utils.messages import (
    ADMIN_MESSAGE_TEXT,
    LABEL_APPEAL_NUMBER,
    LABEL_ADDRESS,
    LABEL_CATEGORY,
    LABEL_DATE,
    LABEL_DESCRIPTION,
    LABEL_REJECT_REASON,
    LABEL_STATUS,
    NO_APPEALS_TEXT,
    REJECT_REASON_EMPTY,
    STATUS_ACCEPTED,
    STATUS_COMPLETED,
    STATUS_IN_PROGRESS,
    STATUS_PENDING,
    STATUS_REJECTED,
    TEXT_MISSING,
)

router = Router()
database = DataBase()


class ViewStates(StatesGroup):
    view_appeals = State()


async def get_formatted_text(user_id: int, offset: int, state: FSMContext):
    appeals = await database.get_user_appeals(
        user_id,
        limit=1,
        offset=offset,
    )

    if not appeals:
        return None

    appeal = appeals[0]
    total = await database.get_user_appeals_count(user_id)
    appeal_status = appeal.get("status")

    await state.update_data(last_appeal_id=appeal.get("id"))

    status = STATUS_PENDING
    if appeal_status == "accepted" or appeal_status == "deferred":
        status = STATUS_ACCEPTED
    elif appeal_status == "in_process":
        status = STATUS_IN_PROGRESS
    elif appeal_status == "rejected":
        status = STATUS_REJECTED
    elif appeal_status == "completed":
        status = STATUS_COMPLETED

    address_block = ""
    if appeal.get("geo_text"):
        address = appeal.get("geo_text")
        address_block = f"\n{LABEL_ADDRESS} {address}"

    reject_block = ""
    if appeal.get("status") == "rejected":
        reject_reason = appeal.get("resolution_message") or REJECT_REASON_EMPTY
        reject_block = (
            f"\n\n{LABEL_REJECT_REASON}\n{html.escape(reject_reason)}"
        )

    caption = (
        f"{LABEL_STATUS} {status}\n\n"
        f"{LABEL_APPEAL_NUMBER} {appeal['id']}\n"
        f"{LABEL_DATE} {format_datetime(appeal['created_at'])}\n"
        f"{LABEL_CATEGORY} {appeal['category']}\n"
        f"{LABEL_DESCRIPTION} {appeal['message']}"
        f"{address_block}"
        f"{reject_block}"
    )

    return {
        "photo": appeal.get("media_id") if appeal.get("media_type") == "photo" else None,
        "video": appeal.get("media_id") if appeal.get("media_type") == "video" else None,
        "text": caption,
        "reply_markup": get_switch_kb(offset + 1, total, appeal.get("status") == 'completed')
    }


async def switch_appeals(callback: CallbackQuery, state: FSMContext, page: int):
    await callback.answer()

    ctx = await UIContext.from_callback(callback, database)

    data = await get_formatted_text(ctx.user_id, page, state)
    if not data:
        msg = await ctx.update_message(
            text=NO_APPEALS_TEXT,
            reply_markup=g_main_menu_kb
        )
        await update_last_message(database, ctx.user_id, msg)
        return

    msg = await ctx.update_message(**data)

    await update_last_message(database, ctx.user_id, msg)

    await state.update_data(page=page)


@router.callback_query(F.data == Callback.VIEW_APPEALS)
async def handle_view_appeals(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(ViewStates.view_appeals)
    await switch_appeals(callback, state, 0)


@router.callback_query(F.data == Callback.APPEAL_NEXT)
async def handle_next_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    total = await database.get_user_appeals_count(callback.from_user.id)
    page = await state.get_value("page", None)

    if page is None or page == total - 1:
        return
    page += 1

    await switch_appeals(callback, state, page)


@router.callback_query(F.data == Callback.APPEAL_PREV)
async def handle_prev_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    page = await state.get_value("page", None)

    if page is None or page == 0:
        return
    page -= 1

    await switch_appeals(callback, state, page)


@router.callback_query(F.data == Callback.DELETE_APPEAL)
async def handle_reject_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    last_appeal_id = await state.get_value("last_appeal_id", None)

    if last_appeal_id is None:
        return

    await database.delete_appeal(last_appeal_id)
    await state.update_data(last_appeal_id=None)

    await handle_view_appeals(callback, state)


@router.callback_query(F.data == Callback.CHECK_INFO)
async def optional_info(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    page = await state.get_value("page", None)
    last_appeal_id = await state.get_value("last_appeal_id", None)
    
    if last_appeal_id is None:
        return
    
    ctx = await UIContext.from_callback(callback, database)
    
    appeal = await ctx.db.get_appeal_by_id(last_appeal_id)
    
    text = appeal.get("resolution_message") or TEXT_MISSING
    
    media = await ctx.db.get_admin_media_by_appeal_id(last_appeal_id)

    media_id = media.get("media_id")
    media_type = media.get("media_type")
    
    msg = await ctx.update_message(
        text=ADMIN_MESSAGE_TEXT.format(text=html.escape(text)),
        photo=media_id if media_type == 'photo' else None,
        video=media_id if media_type == 'video' else None,
        reply_markup=u_info_kb
    )
    await update_last_message(ctx.db, ctx.user_id, msg)


@router.callback_query(F.data == Callback.U_BACK_TO_APPEAL)
async def back_to_appeal(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    page = await state.get_value("page", None)
    await switch_appeals(callback, state, page)
