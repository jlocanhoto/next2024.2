import time
from time import sleep

from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from starlette.middleware.base import RequestResponseEndpoint

app = FastAPI()


class ServerInfo(BaseModel):
    version: str
    name: str
    release_date: str


class UserInfo(BaseModel):
    name: str
    age: int


@app.middleware('http')
async def add_process_time_header(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    print('add_process_time_header')
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


@app.middleware('http')
async def check_authorization_header(
    request: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    print('check_authorization_header')
    authorization = request.headers.get('Accept')
    print('Authorization =', authorization)
    response = await call_next(request)
    return response


@app.get('/')
async def get_server_info() -> ServerInfo:
    sleep(1)
    return ServerInfo(
        version='1.5.2',
        name='NExT 2024.2 Server',
        release_date='2024-11-18',
    )


@app.get('/')
async def get_user_info() -> UserInfo:
    return UserInfo(
        name='João Canhoto',
        age=30,
    )
