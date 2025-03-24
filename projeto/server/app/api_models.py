from pydantic import BaseModel


class ContactApiResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str


class ContactApiRequest(BaseModel):
    name: str
    email: str
    phone: str
