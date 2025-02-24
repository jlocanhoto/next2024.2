"""Objetivo:

Entender como receber dados e parâmetros com o FastAPI."""

from uuid import uuid4

from fastapi import FastAPI

from .json_schema import JsonSchema

app = FastAPI()


# Query Params
# GET http://localhost:8000/songs?offset=50&limit=10
@app.get('/songs')
async def get_songs_list(offset: int, limit: int):
    return {'message': f'Retornando {limit} músicas iniciando a partir da {offset + 1}a. posição'}


# Path Params
@app.get('/songs/{song_id}')
# GET http://localhost:8000/songs/1234
async def get_song_info(song_id: str):
    return {'message': f'Retornando dados da música de id {song_id}'}


# Query e Path Params juntos
# @app.get('/songs/{song_id}')
# async def get_song_info(song_id: str, lang: str | None = None):
#     return {
#         'message': (
#             f'Retornando dados da música de id {song_id} '
#             f'no idioma {"en-US" if lang is None else lang}'
#         )
#     }


class Song(JsonSchema):
    id: str | None = None
    name: str
    authors: list[str]
    album: str
    year: int
    duration_in_seconds: int


# Request Body
@app.post('/songs')
async def add_song(song: Song) -> Song:
    _id = str(uuid4())

    return Song(
        id=_id,
        name=song.name,
        authors=song.authors,
        album=song.album,
        year=song.year,
        duration_in_seconds=song.duration_in_seconds,
    )
    # or
    # return Song(id=_id, **song.model_dump())
