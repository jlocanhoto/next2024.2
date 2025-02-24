"""Objetivo:

Entender como fazer rotas do tipo CRUD, visualizando no /docs o efeito das alterações feitas
em código, aplicando os parâmetros do FastAPI (path, description, response_model, status_code).

CRUD Routes
-----------

GET     /users      Returns the entire array *
GET     /users/:id  Returns an object by its id property
POST    /users      Inserts a new object in the array (autogenerated if not provided)
PUT     /users/:id  Performs a full object update by its id (replace)
DELETE  /users/:id  Deletes an object by its id."""

from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import pratica02 as db_sql

app = FastAPI()


class UserApi(BaseModel):
    id: int
    username: str
    email: str


class UserApiRequest(BaseModel):
    username: str
    email: str
    password: str


@app.get('/users')
async def get_all_users() -> list[UserApi]:
    db_session = db_sql.get_db_session()
    db_users = db_sql.list_users(db_session)

    return [
        UserApi(id=db_user.id, username=db_user.username, email=db_user.email)
        for db_user in db_users
    ]


@app.post('/users', status_code=HTTPStatus.CREATED)
async def add_user(user: UserApiRequest) -> UserApi:
    db_session = db_sql.get_db_session()

    try:
        new_user = db_sql.add_new_user(
            db_session,
            username=user.username,
            password=user.password,
            email=user.email,
        )
        return UserApi(id=new_user.id, username=new_user.username, email=new_user.email)
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(error))


@app.get('/users/{user_id}')
async def get_user(user_id: int) -> UserApi:
    db_session = db_sql.get_db_session()
    user = db_sql.get_user(db_session, user_id)

    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado!')

    return UserApi(
        id=user.id,
        username=user.username,
        email=user.email,
    )


@app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int) -> None:
    db_session = db_sql.get_db_session()

    try:
        db_sql.delete_user(db_session, user_id)
    except KeyError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error))


@app.put('/users/{user_id}')
async def update_user(user_id: int, user: UserApiRequest) -> UserApi:
    db_session = db_sql.get_db_session()

    try:
        db_sql.update_user(
            db_session,
            user_id,
            new_user=db_sql.User(username=user.username, password=user.password, email=user.email),
        )
        return UserApi(id=user_id, username=user.username, email=user.email)
    except (KeyError, ValueError) as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error))
