"""Objetivo:

Entender o que é CRUD e como aplicar os métodos HTTP com o FastAPI."""

from fastapi import FastAPI

app = FastAPI()

# CRUD methods


@app.post('/')
async def create():
    return {'message': 'NExT 2025'}


@app.get('/')
async def read():
    return {'message': 'NExT 2025'}


@app.put('/')
async def update():
    return {'message': 'NExT 2025'}


@app.delete('/')
async def delete():
    return {'message': 'NExT 2025'}


# Other methods


@app.patch('/')
async def update_partially():
    return {'message': 'NExT 2025'}


@app.head('/')
async def head():
    return {'message': 'NExT 2025'}


@app.options('/')
async def options():
    return {'message': 'NExT 2025'}


@app.trace('/')
async def trace():
    return {'message': 'NExT 2025'}
