from pydantic import BaseModel


class Person(BaseModel):
    nome: str
    cpf: str
    genero: str
    email: str
    senha: str
    dataNascimento: str
