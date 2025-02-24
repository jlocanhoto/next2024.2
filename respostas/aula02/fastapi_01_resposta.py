"""Objetivo:

Primeiro contato com o FastAPI com um endpoint que retorna um JSON simples."""

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def hello_world():
    """Descricao do endpoint."""
    return {'message': 'NExT 2025'}
