from typing import Annotated
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from src.entities.customer import Customer
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from src.auth import model
from src.exceptions import AuthenticationError
from dotenv import load_dotenv
import jwt
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 180

oauth2_bearer = HTTPBearer()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verify_password(password_str: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(password_str, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def authenticate_customer(email: str, password: str, db: Session) -> Customer | bool:
    customer = db.query(Customer).filter(Customer.email == email).first()
    if not customer or not verify_password(password, customer.password):
        return False
    return customer

def create_access_token(email: str, customer_id: UUID, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'id': str(customer_id),
        'exp': datetime.now(timezone.utc) + expires_delta
    }

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> model.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        customer_id = payload.get('id')
        return model.TokenData(customer_id=customer_id)
    except jwt.PyJWTError as e:
        return AuthenticationError(e)

def get_current_customer(credentials: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_bearer)]) -> model.TokenData:
    return verify_token(credentials.credentials)

CurrentCustomer = Annotated[model.TokenData, Depends(get_current_customer)]

def login(db: Session, form_data: model.LoginRequest) -> model.Token:
    customer = authenticate_customer(form_data.email, form_data.password, db)
    if not customer:
        raise AuthenticationError()
    token = create_access_token(customer.email, customer.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return model.Token(access_token=token, token_type='bearer')