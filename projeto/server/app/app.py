"""
GET /api/v1/contacts
    exemplo de payload de requisição: NENHUM
    exemplo de payload de resposta: [{"id": 1, "name": "joao", "email": "joao@email", "phone": "(81) 99999-8888"}, {"id": 2, "name": "lucas", "email": "lucas@email", "phone": "(81) 99999-8888"}]
    status da resposta de sucesso: 200 OK

POST /api/v1/contacts
    exemplo de payload de requisição: {"name": "joao", "email": "joao@email", "phone": "(81) 99999-8888"}
    exemplo de payload de resposta: {"id": 1, "name": "joao", "email": "joao@email", "phone": "(81) 99999-8888"}
    status da resposta de sucesso: 201 Created

DELETE /api/v1/contacts/{contact_id}
    exemplo de payload de requisição: NENHUM
    exemplo de payload de resposta: NENHUM
    status da resposta de sucesso: 204 No Content
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from . import db_utils
from .api_models import ContactApiRequest, ContactApiResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/api/v1/contacts')
async def list_contacts() -> list[ContactApiResponse]:
    db_session = db_utils.get_db_session()
    db_contacts_list = db_utils.get_all_contacts(db_session)

    api_contacts_list = [
        ContactApiResponse(
            id=db_contact.id,
            name=db_contact.name,
            email=db_contact.email,
            phone=db_contact.phone,
        )
        for db_contact in db_contacts_list
    ]

    return api_contacts_list


@app.post('/api/v1/contacts', status_code=status.HTTP_201_CREATED)
async def add_contact(contact: ContactApiRequest) -> ContactApiResponse:
    db_session = db_utils.get_db_session()

    try:
        db_contact = db_utils.add_new_contact(
            db_session, contact.name, contact.email, contact.phone
        )

        return ContactApiResponse(
            id=db_contact.id,
            name=db_contact.name,
            email=db_contact.email,
            phone=db_contact.phone,
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


@app.delete('/api/v1/contacts/{contact_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int) -> None:
    db_session = db_utils.get_db_session()

    try:
        db_utils.delete_contact(db_session, contact_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
