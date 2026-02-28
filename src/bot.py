import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, DATABASE_PATH
from db import DataBase
from handlers import moderator_router, user_router


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dispatcher = Dispatcher(storage=MemoryStorage())

    database = DataBase()
    await database.connect(DATABASE_PATH)

    dispatcher.include_router(user_router)
    dispatcher.include_router(moderator_router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
