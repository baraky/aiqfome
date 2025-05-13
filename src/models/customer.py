from pydantic import BaseModel, EmailStr
from uuid import UUID

class RegisterCustomerRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

class CustomerReponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str