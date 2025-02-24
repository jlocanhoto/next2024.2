from fastapi import APIRouter

from . import items

router = APIRouter(prefix='/v1')
router.include_router(items.router)
