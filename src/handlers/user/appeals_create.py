import html

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message

from db import DataBase
from keyboards.global_kb import Callback, g_main_menu_kb
from keyboards.user_kb import get_category_kb, get_finish_kb
from utils.telegram import (
    update_last_message,
    UIContext
)
from utils.messages import (
    APPEAL_CANCELLED_TEXT,
    APPEAL_SENT_TEXT,
    CANCEL,
    CHECK_BEFORE_SUBMIT_TEXT,
    INVALID_CATEGORY_TEXT,
    LABEL_ADDRESS,
    LABEL_CATEGORY,
    LABEL_COORDINATES,
    LABEL_DESCRIPTION,
    NO_ACTIVE_APPEAL_TEXT,
    OUTDATED_APPEAL_TEXT,
    PHOTO_REQUIRED_TEXT,
    PLACEHOLDER_DASH,
    SHORT_DESCRIPTION_TEXT,
    STEP_CATEGORY_SELECT_TEXT,
    STEP_CUSTOM_CATEGORY_TEXT,
    STEP_DESCRIPTION_TEXT,
    STEP_LOCATION_TEXT,
    STEP_PHOTO_TEXT,
)

router = Router()
database = DataBase()


class AppealStates(StatesGroup):
    category = State()
    custom_category = State()
    message = State()
    photo = State()
    location = State()
    finish = State()



async def _update_ui(message: Message | CallbackQuery, text: str, **kwargs) -> None:
    if isinstance(message, Message):
        ctx = await UIContext.from_message(message, database)
    else:
        ctx = await UIContext.from_callback(message, database)
    
    msg = await ctx.update_message(
        text=text,
        **kwargs,
    )
    
    await update_last_message(database, ctx.user_id, msg)


async def _send_preview(message: Message, state: FSMContext, latitude: float | None = None, longitude: float | None = None) -> None:
    data = await state.get_data()

    caption_lines = [
        f"{LABEL_CATEGORY} {data.get('category', PLACEHOLDER_DASH)}",
        f"{LABEL_DESCRIPTION} {data.get('message_text', PLACEHOLDER_DASH)}",
    ]
    if latitude is not None and longitude is not None:
        caption_lines.append(f"{LABEL_COORDINATES} {latitude:.5f}, {longitude:.5f}")
    else:
        caption_lines.append(f"{LABEL_ADDRESS} {data.get('address_msg', PLACEHOLDER_DASH)}")

    photo = await message.answer_photo(
        photo=data["file_id"],
        caption="\n".join(caption_lines),
        parse_mode="HTML",
        reply_markup=get_finish_kb(latitude, longitude),
    )
    await state.update_data(last_bot_photo_id=photo.message_id)


async def _cancel_appeal_flow(ctx: UIContext, state: FSMContext) -> bool:
    current_state = await state.get_state()
    if current_state is None:
        return False

    last_photo_id = await state.get_value("last_bot_photo_id")
    if last_photo_id:
        await ctx.delete(last_photo_id)

    msg = await ctx.update_message(
        text=APPEAL_CANCELLED_TEXT,
        reply_markup=g_main_menu_kb,
    )
    await update_last_message(database, ctx.user_id, msg)
    await state.clear()
    return True


@router.callback_query(F.data == Callback.CREATE_APPEAL)
async def handle_create_appeal_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await _update_ui(
        callback,
        STEP_CATEGORY_SELECT_TEXT,
        reply_markup=get_category_kb(),
    )
    await state.set_state(AppealStates.category)


@router.message(
    StateFilter(   
        AppealStates.category,
        AppealStates.custom_category,
        AppealStates.message,
        AppealStates.photo,
        AppealStates.location,
        AppealStates.finish
    ), 
    Command("cancel")
)
async def handle_cancel_text(message: Message, state: FSMContext):
    ctx = await UIContext.from_message(message, database)
    await _cancel_appeal_flow(ctx, state)


@router.callback_query(AppealStates.category, F.data.startswith("category_"))
async def handle_category_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.update_data(category=callback.data.replace("category_", ""))
    await _update_ui(
        callback,
        STEP_DESCRIPTION_TEXT,
    )
    await state.set_state(AppealStates.message)


@router.callback_query(AppealStates.category, F.data == Callback.CUSTOM_CATEGORY)
async def handle_custom_category_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await _update_ui(
        callback,
        STEP_CUSTOM_CATEGORY_TEXT,
    )
    await state.set_state(AppealStates.custom_category)


@router.message(AppealStates.custom_category)
async def handle_custom_category_input(message: Message, state: FSMContext):
    text = html.escape((message.text or "").strip())

    if not 3 <= len(text) <= 30:
        await _update_ui(
            message,
            INVALID_CATEGORY_TEXT,
        )
        return

    await state.update_data(category=text)
    await _update_ui(
        message,
        STEP_DESCRIPTION_TEXT,
    )
    await state.set_state(AppealStates.message)


@router.message(AppealStates.message)
async def handle_problem_description_input(message: Message, state: FSMContext):
    text = html.escape((message.text or "").strip())

    if len(text) < 10:
        await _update_ui(
            message,
            SHORT_DESCRIPTION_TEXT,
        )
        return

    await state.update_data(message_text=text)
    await _update_ui(
        message,
        STEP_PHOTO_TEXT,
    )
    await state.set_state(AppealStates.photo)


@router.message(AppealStates.photo)
async def handle_problem_photo_input(message: Message, state: FSMContext):
    if not message.photo:
        await _update_ui(
            message,
            PHOTO_REQUIRED_TEXT,
        )
        return

    await state.update_data(file_id=message.photo[-1].file_id)
    await _update_ui(
        message,
        STEP_LOCATION_TEXT
    )
    await state.set_state(AppealStates.location)


@router.message(AppealStates.location, F.text)
async def handle_address_input(message: Message, state: FSMContext):
    address_text = html.escape(message.text)

    await state.update_data(address_msg=address_text, latitude=None, longitude=None)
    await state.set_state(AppealStates.finish)

    await _update_ui(message, CHECK_BEFORE_SUBMIT_TEXT)
    await _send_preview(message, state)


@router.message(AppealStates.location, F.location)
async def handle_problem_location_input(message: Message, state: FSMContext):
    latitude = message.location.latitude
    longitude = message.location.longitude
    
    await state.update_data(latitude=latitude, longitude=longitude)
    await state.set_state(AppealStates.finish)

    await _update_ui(message, CHECK_BEFORE_SUBMIT_TEXT)
    await _send_preview(message, state, latitude=latitude, longitude=longitude)


@router.callback_query(F.data == Callback.CANCEL_CREATE_APPEAL)
async def handle_appeal_cancel_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    ctx = await UIContext.from_callback(callback, database)
    await _cancel_appeal_flow(ctx, state)
    
    
@router.message(Command("cancel"))
async def cancel_appeal_create(message: Message, state: FSMContext):
    ctx = await UIContext.from_message(message, database)
    await _cancel_appeal_flow(ctx, state)
    

@router.callback_query(F.data == Callback.SUCCESS_CREATE_APPEAL)
async def handle_appeal_confirm_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    ctx = await UIContext.from_callback(callback, database)

    await ctx.delete(data.get("last_bot_photo_id"))

    if not data or "category" not in data:
        msg = await ctx.update_message(
            text=OUTDATED_APPEAL_TEXT,
            reply_markup=g_main_menu_kb,
        )
        
        await update_last_message(database, ctx.user_id, msg)
        return

    await database.create_appeal(
        tg_id=ctx.user_id,
        username=ctx.username,
        category=data["category"],
        message=data["message_text"],
        media_id=data["file_id"],
        media_type="photo",
        geo_text=data.get("address_msg"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )

    msg = await ctx.update_message(
        text=APPEAL_SENT_TEXT,
        reply_markup=g_main_menu_kb,
    )
    
    await update_last_message(database, ctx.user_id, msg)
    await state.clear()
