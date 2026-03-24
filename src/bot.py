import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import BOT_TOKEN, DATABASE_URL, REDIS_URL
from db import DataBase
from handlers import (
    moderator_router, 
    user_router, 
    admin_router, 
    owner_router
)
from middlewares import (
    BanMiddleware,
    AutodeleteMiddleware,
    CheckModerator,
    CheckAdmin,
    CheckOwner,
    AddUser
)


async def cleanup_task(database):
    while True:
        await database.cleanup_role_invites()
        await asyncio.sleep(600)


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    
    if REDIS_URL:
        redis = Redis.from_url(REDIS_URL)
        storage = RedisStorage(redis=redis)
    else:
        storage = MemoryStorage()
        
    dispatcher = Dispatcher(storage=storage)

    database = DataBase()
    await database.connect(DATABASE_URL)
    
    dispatcher.update.middleware(AddUser(database))
    dispatcher.update.middleware(AutodeleteMiddleware())
    dispatcher.update.middleware(BanMiddleware(database))
    dispatcher.callback_query.middleware(CheckModerator(database))
    dispatcher.callback_query.middleware(CheckAdmin(database))
    dispatcher.callback_query.middleware(CheckOwner())
    
    dispatcher.include_routers(
        user_router,
        moderator_router,
        admin_router,
        owner_router
    )
    
    asyncio.create_task(cleanup_task(database))

    await dispatcher.start_polling(
        bot,
        polling_timeout=60,
        allowed_updates=dispatcher.resolve_used_update_types(),
    )


if __name__ == "__main__":
    asyncio.run(main())
