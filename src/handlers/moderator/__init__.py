from aiogram import Router

from .moderator import router as moderator_router

router = Router()

router.include_router(moderator_router)
