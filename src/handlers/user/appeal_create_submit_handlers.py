from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from handlers.common import answer, cancel_appeal_flow, delete_message, update_last_message, update_message
from keyboards.global_kb import Callback, g_main_menu_kb
from keyboards.user_kb import get_finish_kb, u_location_kb
from utils import get_chat_id, get_user_id

from .appeal_create_common import AppealStates, database, router


@router.message(AppealStates.message)
async def handle_problem_description_input(message: Message, state: FSMContext):
    await message.delete()
    text = (message.text or "").strip()

    if len(text) < 10:
        msg = await update_message(
            bot=message.bot,
            chat_id=get_chat_id(message),
            message_id=await state.get_value("last_bot_message_id"),
            text=(
                "❌ <b>Слишком короткое описание</b>\n"
                "Текст должен содержать минимум 10 символов. Попробуйте снова."
            )
        )
        await update_last_message(state, msg)
        return

    await state.update_data(message_text=text)

    msg = await update_message(
        bot=message.bot,
        chat_id=get_chat_id(message),
        message_id=await state.get_value("last_bot_message_id"),
        text="<b>Шаг 3 из 4. Фотография</b>\nОтправьте фотографию проблемы."
    )
    await update_last_message(state, msg)
    
    await state.set_state(AppealStates.photo)


@router.message(AppealStates.photo)
async def handle_problem_photo_input(message: Message, state: FSMContext):
    await message.delete()

    if not message.photo:
        msg = await update_message(
            bot=message.bot,
            chat_id=get_chat_id(message),
            message_id=await state.get_value("last_bot_message_id"),
            text="❌ <b>Нужна фотография</b>\nПожалуйста, отправьте изображение."
        )
        await update_last_message(state, msg)
        return

    await state.update_data(file_id=message.photo[-1].file_id)
    msg = await update_message(
        bot=message.bot,
        chat_id=get_chat_id(message),
        message_id=await state.get_value("last_bot_message_id"),
        text=(
            "<b>Шаг 4 из 4. Геопозиция</b>\n"
            "Отправьте геолокацию через телеграм или введите адрес вручную"
        )
    )
    await update_last_message(state, msg)
    await state.set_state(AppealStates.location)
    
    
@router.message(AppealStates.location, F.text)
async def handle_address_input(message: Message, state: FSMContext):
    msg = message.text
    await message.delete()
    
    await state.update_data(address_msg=msg, latitude=None, longitude=None)
    data = await state.get_data()
    
    await state.set_state(AppealStates.finish)
    
    msg = await update_message(
        bot=message.bot,
        chat_id=get_chat_id(message),
        message_id=await state.get_value("last_bot_message_id"),
        text="<b>Проверьте данные перед отправкой</b>"
    )
    await update_last_message(state, msg)

    photo = await message.answer_photo(
        photo=data["file_id"],
        caption=(
            f"🗂 <b>Категория:</b> {data.get('category', '—')}\n"
            f"📝 <b>Описание:</b> {data.get('message_text', '—')}\n"
            f"📍 <b>Адрес:</b> {data.get("address_msg", "—")}"
        ),
        parse_mode="HTML",
        reply_markup=get_finish_kb(),
    )

    await state.update_data(last_bot_photo_id=photo.message_id)
    

@router.message(AppealStates.location, F.location)
async def handle_problem_location_input(message: Message, state: FSMContext):
    await message.delete()

    latitude = message.location.latitude
    longitude = message.location.longitude
    await state.update_data(latitude=latitude, longitude=longitude)
    data = await state.get_data()
    
    await state.set_state(AppealStates.finish)
    
    msg = await update_message(
        bot=message.bot,
        chat_id=get_chat_id(message),
        message_id=await state.get_value("last_bot_message_id"),
        text="<b>Проверьте данные перед отправкой</b>"
    )
    await update_last_message(state, msg)

    photo = await message.answer_photo(
        photo=data["file_id"],
        caption=(
            f"🗂 <b>Категория:</b> {data.get('category', '—')}\n"
            f"📝 <b>Описание:</b> {data.get('message_text', '—')}\n"
            f"📍 <b>Координаты:</b> {latitude:.5f}, {longitude:.5f}"
        ),
        parse_mode="HTML",
        reply_markup=get_finish_kb(latitude, longitude),
    )

    await state.update_data(last_bot_photo_id=photo.message_id)


@router.message(AppealStates.finish)
async def block_messages_on_finish(message: Message):
    await message.delete()


@router.callback_query(F.data == Callback.CANCEL_CREATE_APPEAL)
async def handle_appeal_cancel_click(callback: CallbackQuery, state: FSMContext):
    await delete_message(
        callback.message.bot,
        get_chat_id(callback),
        await state.get_value("last_bot_message_id"),
    )
    await callback.answer()
    await cancel_appeal_flow(callback.message, state)


@router.callback_query(F.data == Callback.SUCCESS_CREATE_APPEAL)
async def handle_appeal_confirm_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()

    await delete_message(
        callback.message.bot,
        get_chat_id(callback),
        data.get("last_bot_photo_id"),
    )

    if not data or "category" not in data:
        msg = await update_message(
            bot=callback.message.bot,
            chat_id=get_chat_id(callback),
            message_id=data.get("last_bot_message_id"),
            text=(
                "ℹ️ <b>Обращение уже неактуально</b>\n"
                "Создайте новое обращение из главного меню."
            ),
            reply_markup=g_main_menu_kb
        )
        await update_last_message(state, msg)
        return

    await database.create_appeal(
        tg_id=get_user_id(callback),
        category=data["category"],
        message=data["message_text"],
        photo_id=data["file_id"],
        geo_text=data.get("address_msg"),
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )

    msg = await update_message(
        bot=callback.message.bot,
        chat_id=get_chat_id(callback),
        message_id=await state.get_value("last_bot_message_id"),
        text=(
            "✅ <b>Обращение отправлено</b>\n"
            "Заявка передана на модерацию ЖК «Янино-1».\n"
            "Если понадобятся уточнения, мы свяжемся с вами."
        ),
        reply_markup=g_main_menu_kb
    )
    await update_last_message(state, msg)