from fastapi import APIRouter
from starlette import status
from src.models.favorite import FavoriteReponse, FavoriteCreate
from src.db.core import DbSession
from src.auth.service import CurrentCustomer
import src.api.favorites as service

router = APIRouter(
    prefix='/favorites',
    tags=['Favorites']
)

@router.post("/", response_model=FavoriteCreate, status_code=status.HTTP_201_CREATED)
async def create_favorite(db: DbSession, product_id: int, current_customer: CurrentCustomer):
    return await service.add_product_to_favorites(db, product_id, current_customer.get_uuid())

@router.get("/", response_model=list[FavoriteReponse])
async def get_favorites(db: DbSession, current_customer: CurrentCustomer):
    return await service.get_favorites(db, current_customer.get_uuid())

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(db: DbSession, product_id: int, current_customer: CurrentCustomer):
    service.remove_product_from_favorites(db, product_id, current_customer.get_uuid())