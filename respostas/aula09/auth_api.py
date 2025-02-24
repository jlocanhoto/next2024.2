from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from . import db_sql, jwt_utils, password_utils


class Token(BaseModel):
    access_token: str
    token_type: str


class UserApi(BaseModel):
    id: int
    username: str
    email: str


class UserApiRequest(BaseModel):
    username: str
    email: str
    password: str


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


@app.get('/', response_class=HTMLResponse)
async def login_page() -> str:
    with open('./login.html', encoding='utf-8') as fp:
        return fp.read()


@app.post('/signup', status_code=HTTPStatus.CREATED)
async def add_user(user: UserApiRequest) -> UserApi:
    db_session = db_sql.get_db_session()

    try:
        new_user = db_sql.add_new_user(
            db_session,
            username=user.username,
            password=password_utils.hash_password(user.password),
            email=user.email,
        )
        return UserApi(id=new_user.id, username=new_user.username, email=new_user.email)
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(error))


@app.post('/login')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    auth_fail_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='As credenciais estão incorretas!',
    )

    db_session = db_sql.get_db_session()
    username_or_email = form_data.username
    db_user = db_sql.get_user_by_username_or_email(db_session, username_or_email, username_or_email)

    if db_user is None:
        raise auth_fail_exception

    if not password_utils.validate_password(form_data.password, db_user.password):
        raise auth_fail_exception

    token = jwt_utils.create_jwt(str(db_user.id), expires_secs=3600)

    return Token(access_token=token, token_type='bearer')


# def get_current_user(token: str) -> db_sql.User:
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    invalid_credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Credenciais inválidas!',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    payload = jwt_utils.validate_jwt(token)

    if payload is None:
        raise invalid_credentials_exception

    user_id = int(payload.get('sub', -1))

    db_session = db_sql.get_db_session()
    user = db_sql.get_user(db_session, user_id)

    if user is None:
        raise invalid_credentials_exception

    return user


# @app.get('/account')
# async def get_current_account_info(
#     authorization: Annotated[str | None, Header()] = None,
# ) -> UserApi:
#     if authorization is None:
#         raise HTTPException(
#             status_code=HTTPStatus.UNAUTHORIZED,
#             detail='Credenciais inválidas!',
#             headers={'WWW-Authenticate': 'Bearer'},
#         )

#     token = authorization.replace('Bearer ', '')
#     current_db_user = get_current_user(token)

#     return UserApi(
#         id=current_db_user.id,
#         username=current_db_user.username,
#         email=current_db_user.email,
#     )


@app.get('/account')
async def get_current_account_info(
    current_db_user: Annotated[db_sql.User, Depends(get_current_user)],
) -> UserApi:
    return UserApi(
        id=current_db_user.id,
        username=current_db_user.username,
        email=current_db_user.email,
    )
