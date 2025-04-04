"""Objetivo:

Entender como fazer rotas do tipo CRUD, visualizando no /docs o efeito das alterações feitas
em código, aplicando os parâmetros do FastAPI (path, description, response_model, status_code).

CRUD Routes
-----------

GET     /items      Returns the entire array *
GET     /items/:id  Returns an object by its id property
POST    /items      Inserts a new object in the array (autogenerated if not provided)
PUT     /items      Replaces the whole data bucket content
PUT     /items/:id  Performs a full object update by its id (replace)
DELETE  /items      Deletes the data bucket content
DELETE  /items/:id  Deletes an object by its id
PATCH   /items      Concatenates the arrays
PATCH   /items/:id  Performs a partial object update by its id (merge)."""

from http import HTTPStatus
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    id: str | None = None
    name: str | None = None
    price: float | None = None


items_db: dict[str, Item] = {}


@app.get('/items')
async def get_all_items() -> list[Item]:
    return list(items_db.values())


@app.get('/items/{item_id}')
async def get_item(item_id: str) -> Item:
    item = items_db.get(item_id)

    if item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Item not found!')

    return item


@app.post('/items', status_code=HTTPStatus.CREATED)
async def add_item(item: Item) -> Item:
    item.id = str(uuid4())
    items_db[item.id] = item

    return item


@app.put('/items')
async def update_all_items(items: list[Item]) -> list[Item]:
    items_db.clear()

    for item in items:
        if item.id is None:
            item.id = str(uuid4())

        items_db.update({item.id: item})

    return list(items_db.values())


@app.put('/items/{item_id}')
async def update_item(item_id: str, item: Item) -> Item:
    if item_id not in items_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=f"Item {item_id} doesn't exist in DB!"
        )

    item.id = item_id
    items_db[item_id] = item
    return item


@app.delete('/items', status_code=HTTPStatus.NO_CONTENT)
async def delete_all() -> None:
    items_db.clear()


@app.delete('/items/{item_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_item(item_id: str) -> None:
    if items_db.get(item_id) is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Item {item_id} doesn't exist in DB!"
        )

    del items_db[item_id]


@app.patch('/items')
async def update_some_items(items: list[Item]) -> list[Item]:
    for item in items:
        if item.id is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Missing item id')

        items_db[item.id] = item

    return items


@app.patch('/items/{item_id}')
async def update_item_partially(item_id: str, item: Item) -> Item:
    stored_item = items_db[item_id]
    item_params_to_update = item.model_dump(exclude_unset=True)
    updated_item = stored_item.model_copy(update=item_params_to_update)
    items_db[item_id] = updated_item
    return updated_item
