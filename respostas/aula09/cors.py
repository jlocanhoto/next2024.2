from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class UserApi(BaseModel):
    id: int
    username: str
    email: str


app = FastAPI()

origins = [
    'http://localhost:5500',
    'http://127.0.0.1:5500',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', response_class=HTMLResponse)
async def home_page() -> str:
    with open('./account.html', encoding='utf-8') as fp:
        return fp.read()


@app.get('/api/account')
async def get_current_account_info() -> UserApi:
    return UserApi(
        id=1,
        username='canhoto',
        email='canhoto@gmail.com',
    )
