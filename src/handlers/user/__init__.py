from aiogram import Router

from .appeal_create import router as appeal_create_router
from .appeal_view import router as appeal_view_router
from .start import router as start_router

router = Router()

router.include_router(start_router)
router.include_router(appeal_create_router)
router.include_router(appeal_view_router)
