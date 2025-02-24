from uuid import uuid4

from fastapi import FastAPI

from .pydantic_04_resposta import Person

app = FastAPI()


@app.post('/cadastro')
async def fazer_cadastro(person: Person) -> Person:
    person.id = str(uuid4())
    return person
