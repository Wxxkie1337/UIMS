import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database import DataBase
from config import BOT_TOKEN, DATABASE_PATH
# from handlers.user import user_router
# from handlers.admin import admin_router
# from handlers.moderator import moderator_router

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    db = DataBase()

    await db.connect(DATABASE_PATH)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())