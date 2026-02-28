from .moderator import router as moderator_router
from .user import router as user_router

# from .admin import router as admin_router

__all__ = (
    "user_router",
    "moderator_router",
)
