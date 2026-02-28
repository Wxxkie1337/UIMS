from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.common import answer, delete_message
from keyboards.global_kb import Callback
from keyboards.user_kb import get_category_kb
from utils import get_chat_id

from .appeal_create_common import AppealStates, router


@router.callback_query(F.data == Callback.CREATE_APPEAL)
async def handle_create_appeal_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await answer(
        text="<b>Шаг 1 из 4. Категория</b>\nВыберите категорию проблемы.",
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
        text="<b>Шаг 2 из 4. Описание</b>\nОпишите проблему подробно (минимум 10 символов).",
        message=callback.message,
        state=state,
    )

    await state.set_state(AppealStates.message)


@router.callback_query(AppealStates.category, F.data == Callback.CUSTOM_CATEGORY)
async def handle_custom_category_click(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    await answer(
        text="<b>Шаг 1 из 4. Категория</b>\nВведите свою категорию проблемы.",
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
                "❌ <b>Некорректная категория</b>\n"
                "Название должно содержать от 3 до 30 символов. Попробуйте снова."
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
        text="<b>Шаг 2 из 4. Описание</b>\nОпишите проблему подробно (минимум 10 символов).",
        message=message,
        state=state,
    )
    await state.set_state(AppealStates.message)
