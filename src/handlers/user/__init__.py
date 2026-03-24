from aiogram import Router

from .appeals_create import router as appeals_create_router
from .appeals_view import router as appeals_view_router
from .start import router as start_router

router = Router()

router.include_router(start_router)
router.include_router(appeals_create_router)
router.include_router(appeals_view_router)
