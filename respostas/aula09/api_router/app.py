from fastapi import APIRouter, FastAPI

from .routers import v1, v2

app = FastAPI()

api_router = APIRouter(prefix='/api')
api_router.include_router(v1.router)
api_router.include_router(v2.router)

app.include_router(api_router)
