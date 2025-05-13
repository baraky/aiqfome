from typing import Annotated
from fastapi import APIRouter, Depends
from src.auth import model
from src.auth import service
from fastapi.security import OAuth2PasswordRequestForm
from src.db.core import DbSession

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)

@router.post("/login", response_model=model.Token)
async def login(db: DbSession, form_data: model.LoginRequest):
    return service.login(db, form_data)