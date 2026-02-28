from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from db import DataBase
from handlers.common import answer, cancel_appeal_flow, delete_message
from keyboards.global_kb import Callback, g_main_menu_kb
from keyboards.user_kb import get_category_kb, get_finish_kb, u_location_kb
from utils import get_chat_id, get_user_id

router = Router()
database = DataBase()


class AppealStates(StatesGroup):
    category = State()
    custom_category = State()
    message = State()
    photo = State()
    location = State()
    finish = State()


@router.callback_query(F.data == Callback.CREATE_APPEAL)
async def handle_create_appeal_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await answer(
        text=f"📂 Выберите категорию проблемы:",
        message=callback.message,
        state=state,
        reply_markup=get_category_kb(),
    )

    await state.set_state(AppealStates.category)


@router.callback_query(AppealStates.category, F.data.startswith("category_"))
async def handle_category_selected(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await state.update_data(category=callback.data.replace("category_", ""))

    await answer(
        text=f"📝 Опишите проблему подробно (не менее 10 символов):",
        message=callback.message,
        state=state,
    )

    await state.set_state(AppealStates.message)


@router.callback_query(AppealStates.category, F.data == Callback.CUSTOM_CATEGORY)
async def handle_custom_category_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await answer(
        text=f"✏️ Напишите свою категорию проблемы",
        message=callback.message,
        state=state,
    )

    await state.set_state(AppealStates.custom_category)


@router.message(AppealStates.custom_category)
async def handle_custom_category_input(message: Message, state: FSMContext):
    await message.delete()

    text = (message.text or "").strip()

    if not 3 <= len(text) <= 30:
        await delete_message(
            message.bot,
            get_chat_id(message),
            await state.get_value("last_bot_message_id"),
        )
        await answer(
            text=(
                f"❌ Категория должна содержать от 3 до 30 символов.\n"
                f"Попробуйте ещё раз:"
            ),
            message=message,
            state=state,
        )
        return

    await state.update_data(category=text)

    await delete_message(
        message.bot,
        get_chat_id(message),
        await state.get_value("last_bot_message_id"),
    )

    await answer(
        text=f"📝 Опишите проблему подробно (не менее 10 символов):",
        message=message,
        state=state,
    )

    await state.set_state(AppealStates.message)


@router.message(AppealStates.message)
async def handle_problem_description_input(message: Message, state: FSMContext):
    await message.delete()

    text = (message.text or "").strip()

    if len(text) < 10:
        await delete_message(
            message.bot,
            get_chat_id(message),
            await state.get_value("last_bot_message_id"),
        )
        await answer(
            text=(
                f"❌ Описание должно быть не короче 10 символов.\n"
                f"Попробуйте ещё раз:"
            ),
            message=message,
            state=state,
        )
        return

    await state.update_data(message_text=text)

    await delete_message(
        message.bot,
        get_chat_id(message),
        await state.get_value("last_bot_message_id"),
    )

    await answer(
        text=f"📸 Пришлите фото проблемы:",
        message=message,
        state=state,
    )

    await state.set_state(AppealStates.photo)


@router.message(AppealStates.photo)
async def handle_problem_photo_input(message: Message, state: FSMContext):
    await message.delete()

    if not message.photo:
        await delete_message(
            message.bot,
            get_chat_id(message),
            await state.get_value("last_bot_message_id"),
        )
        await answer(
            text=f"❌ Пожалуйста, отправьте именно фотографию:",
            message=message,
            state=state,
        )
        return

    await state.update_data(file_id=message.photo[-1].file_id)

    await delete_message(
        message.bot,
        get_chat_id(message),
        await state.get_value("last_bot_message_id"),
    )

    await answer(
        text=(
            f"📍 Отправьте геопозицию проблемы.\n"
            f"Скрепка 📎 → «Геопозиция» → «Отправить мою геопозицию»"
        ),
        message=message,
        state=state,
        reply_markup=u_location_kb,
    )

    await state.set_state(AppealStates.location)


@router.message(AppealStates.location)
async def handle_problem_location_input(message: Message, state: FSMContext):
    await message.delete()

    if not message.location:
        await delete_message(
            message.bot,
            get_chat_id(message),
            await state.get_value("last_bot_message_id"),
        )
        await answer(
            text=f"❌ Отправьте именно геопозицию:",
            message=message,
            state=state,
            reply_markup=u_location_kb,
        )
        return

    latitude = message.location.latitude
    longitude = message.location.longitude

    await state.update_data(latitude=latitude, longitude=longitude)

    data = await state.get_data()

    await delete_message(
        message.bot,
        get_chat_id(message),
        await state.get_value("last_bot_message_id"),
    )

    await state.set_state(AppealStates.finish)

    msg = await message.answer(
        "✅ Проверьте ваше обращение:",
        reply_markup=ReplyKeyboardRemove(),
    )

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

    await state.update_data(
        last_bot_message_id=msg.message_id, last_bot_photo_id=photo.message_id
    )


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
    await callback.message.delete()
    await cancel_appeal_flow(callback.message, state)


@router.callback_query(F.data == Callback.SUCCESS_CREATE_APPEAL)
async def handle_appeal_confirm_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()

    await delete_message(
        callback.message.bot,
        get_chat_id(callback),
        data["last_bot_message_id"],
    )

    if not data or "category" not in data:
        await callback.message.answer(
            "⏳ Это обращение уже неактуально.\n"
            "Пожалуйста, создайте новое из главного меню.",
            reply_markup=g_main_menu_kb,
        )
        await state.clear()
        return

    await database.create_appeal(
        tg_id=get_user_id(callback),
        category=data["category"],
        message=data["message_text"],
        photo_id=data["file_id"],
        latitude=data["latitude"],
        longitude=data["longitude"],
    )

    await callback.message.delete()
    await state.clear()

    await answer(
        text=(
            "🎉 Спасибо!\n"
            "Ваше обращение успешно отправлено модерации ЖК «Янино-1».\n"
            "Мы свяжемся с вами, если понадобятся уточнения."
        ),
        message=callback.message,
        state=state,
        reply_markup=g_main_menu_kb,
    )
