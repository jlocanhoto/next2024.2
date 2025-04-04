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
from fastapi.responses import HTMLResponse
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


@app.get('/', response_class=HTMLResponse)
async def main_app():
    html_page = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sign-Up Page</title>
            <style>
                body {
                    display: flex;
                    justify-content: space-between;
                    padding: 20px;
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                }
                .form-container, .users-container {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }
                .form-container {
                    width: 40%;
                }
                .users-container {
                    width: 50%;
                }
                h2 {
                    color: #333;
                }
                input {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    background-color: #28a745;
                    color: white;
                    padding: 10px 15px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #218838;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    background: #e9ecef;
                    margin: 5px 0;
                    padding: 10px;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background 0.3s;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                li:hover {
                    background: #d6d8db;
                }
                .btn-container {
                    display: flex;
                    gap: 5px;
                }
                .edit-btn, .delete-btn {
                    padding: 5px 10px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .edit-btn {
                    background-color: #ffc107;
                    color: white;
                }
                .edit-btn:hover {
                    background-color: #e0a800;
                }
                .delete-btn {
                    background-color: #dc3545;
                    color: white;
                }
                .delete-btn:hover {
                    background-color: #c82333;
                }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h2>Sign Up</h2>
                <form id="signup-form">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required>
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                    <button type="submit">Sign Up</button>
                </form>
            </div>

            <div class="users-container">
                <h2>Registered Users</h2>
                <ul id="users-list"></ul>
            </div>

            <script>
                document.getElementById('signup-form').addEventListener('submit', async function(event) {
                    event.preventDefault();

                    const formData = {
                        username: document.getElementById('username').value,
                        email: document.getElementById('email').value,
                        password: document.getElementById('password').value,
                    };

                    try {
                        const response = await fetch('/users', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(formData)
                        });

                        if (!response.ok) {
                            const errorMsg = await response.json();
                            alert(`Erro!\n\n${errorMsg.detail}`);
                        }

                        loadUsers();
                    } catch (error) {
                        console.error(JSON.stringify(error));
                    }
                });

                async function loadUsers() {
                    const response = await fetch('/users');
                    const users = await response.json();

                    const usersList = document.getElementById('users-list');
                    usersList.innerHTML = '';
                    users.forEach(user => {
                        const li = document.createElement('li');
                        li.textContent = `${user.username} (${user.email})`;

                        const btnContainer = document.createElement('div');
                        btnContainer.classList.add('btn-container');

                        const editBtn = document.createElement('button');
                        editBtn.textContent = 'Edit';
                        editBtn.classList.add('edit-btn');
                        editBtn.addEventListener('click', async (event) => {
                            event.stopPropagation();

                            const newName = prompt('Enter new username:', user.username);
                            const newEmail = prompt('Enter new email:', user.email);
                            const newPassword = prompt('Enter new password:');

                            if (newName && newEmail && newPassword) {
                                await fetch(`/users/${user.id}`, {
                                    method: 'PUT',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ username: newName, email: newEmail, password: newPassword })
                                });
                                loadUsers();
                            }
                        });

                        const deleteBtn = document.createElement('button');
                        deleteBtn.textContent = 'Delete';
                        deleteBtn.classList.add('delete-btn');
                        deleteBtn.addEventListener('click', async (event) => {
                            event.stopPropagation();
                            if (confirm('Are you sure you want to delete this user?')) {
                                await fetch(`/users/${user.id}`, {
                                    method: 'DELETE'
                                });
                                loadUsers();
                            }
                        });

                        btnContainer.appendChild(editBtn);
                        btnContainer.appendChild(deleteBtn);

                        li.appendChild(btnContainer);
                        usersList.appendChild(li);
                    });
                }

                loadUsers();
            </script>
        </body>
        </html>
    """

    return html_page
