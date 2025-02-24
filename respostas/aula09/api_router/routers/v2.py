from fastapi import APIRouter

from . import items, users

router = APIRouter(prefix='/v2')
router.include_router(items.router)
router.include_router(users.router)
