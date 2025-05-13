from uuid import UUID
from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    customer_id: str | None = None

    def get_uuid(self) -> UUID | None:
        if self.customer_id:
            return UUID(self.customer_id)
        return None