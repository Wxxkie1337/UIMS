import html

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.global_kb import Callback, g_understand_kb
from keyboards.admin_kb import get_reason_kb, a_cancel_kb, a_cancel_or_success_kb, get_active_appeals_kb, a_adminmenu_kb
from utils.telegram import (
    notify,
    UIContext,
    update_last_message
)
from utils.messages import (
    ADMIN_ACTION_FAILED_TEXT,
    ADMIN_APPEAL_NO_LONGER_ACTIVE_TEXT,
    ADMIN_COMPLETE_INVALID_MESSAGE_TEXT,
    ADMIN_COMPLETE_MEDIA_GROUP_ERROR_TEXT,
    ADMIN_COMPLETE_PREVIEW_TEXT,
    ADMIN_COMPLETED_NOTIFY_TEXT,
    LABEL_APPEAL_NUMBER,
    TEXT_MISSING,
)

from .shared import router, database, AdminStates


@router.message(AdminStates.complete_message, F.text | F.photo | F.video)
async def admin_message_handler(message: Message, state: FSMContext):
    text = message.text or message.caption
    photo = message.photo
    video = message.video
    
    message_id = await state.get_value("msg_id")
    
    ctx = await UIContext.from_message(message, database)
    
    if message.media_group_id:
        msg = await ctx.update_specific(
            message_id=message_id,
            text=ADMIN_COMPLETE_MEDIA_GROUP_ERROR_TEXT,
            reply_markup=a_cancel_kb
        )
        return
    
    photo_id = photo[-1].file_id if photo else None
    video_id = video.file_id if video else None
    
    msg = await ctx.update_specific(
        message_id=message_id,
        text=ADMIN_COMPLETE_PREVIEW_TEXT.format(
            text=html.escape(text or TEXT_MISSING)
        ),
        photo=photo_id,
        video=video_id,
        reply_markup=a_cancel_or_success_kb
    )
    
    await state.update_data(
        msg_id=msg,
        admin_message=text,
        media_id=(video_id or photo_id),
        media_type="video" if video_id else "photo" if photo_id else None
    )
    
    await state.set_state(None)
    
    
@router.message(AdminStates.complete_message)
async def admin_illegal_message_handler(message: Message, state: FSMContext):
    message_id = await state.get_value("msg_id")
    
    ctx = await UIContext.from_message(message, database)
    
    msg = await ctx.update_specific(
        message_id=message_id,
        text=ADMIN_COMPLETE_INVALID_MESSAGE_TEXT,
        reply_markup=a_cancel_kb
    )
    
    await state.update_data(msg_id=msg)
    
    
@router.callback_query(F.data == Callback.A_CANCEL)
async def cancel(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(AdminStates.check_active_appeals)

    try: await callback.message.delete()
    except Exception: pass
    
    
@router.callback_query(F.data == Callback.A_SUCCESS)
async def success(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    text = await state.get_value("admin_message")
    appeal_id = await state.get_value("appeal_id")
    message_id = await state.get_value("msg_id")
    media_id = await state.get_value("media_id")
    media_type = await state.get_value("media_type")
    
    ctx = await UIContext.from_callback(callback, database)
    
    appealer_id = await ctx.db.get_user_id_by_appeal(int(appeal_id))

    if appealer_id and await ctx.db.complete_appeal(int(appeal_id), text):
        if media_id:
            await ctx.db.add_media(appeal_id, media_id, media_type, 'admin')
            
        await notify(
            bot=ctx.bot,
            chat_id=appealer_id,
            text=ADMIN_COMPLETED_NOTIFY_TEXT.format(
                appeal_number=f"{LABEL_APPEAL_NUMBER} {appeal_id}"
            )
        )
        
        await ctx.delete(message_id)
        
        msg = await ctx.update_message(
            text=ADMIN_APPEAL_NO_LONGER_ACTIVE_TEXT,
            reply_markup=a_adminmenu_kb
        )
        await update_last_message(ctx.db, ctx.user_id, msg)
        
        await state.clear()
    else:
        await ctx.update_specific(
            message_id=message_id,
            text=ADMIN_ACTION_FAILED_TEXT,
            reply_markup=g_understand_kb
        )
