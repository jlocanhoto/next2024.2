from fastapi import APIRouter, FastAPI

app = FastAPI()

router = APIRouter(prefix='/items')


@router.get('')
def get_all_items(): ...
