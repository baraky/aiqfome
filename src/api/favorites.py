from src.external_services.products import get_product_by_id
from sqlalchemy.orm import Session
from src.exceptions import *
from src.entities.favorite import Favorite
from src.models.favorite import FavoriteReponse
from src.auth.model import TokenData
from typing import List
from uuid import UUID
import asyncio

async def add_product_to_favorites(db: Session, product_id: int, customer_id: UUID) -> Favorite:
    if not await get_product_by_id(product_id):
        raise ProductNotFoundError(product_id)

    existing_favorite = (
        db.query(Favorite)
        .filter(Favorite.customer_id == customer_id)
        .filter(Favorite.product_id == product_id)
        .first()
    )
    
    if existing_favorite:
        raise ProductAlreadyFavoritedError(product_id)

    try:
        new_favorite = Favorite(product_id=product_id, customer_id=customer_id)
        db.add(new_favorite)
        db.commit()
        db.refresh(new_favorite)

        return new_favorite
    except Exception as e:
        raise FavoriteCreationError(str(e))

async def get_favorite_by_product_id(db: Session, product_id: int, customer_id: UUID) -> FavoriteReponse:
    favorite = (
        db.query(Favorite)
        .filter(Favorite.customer_id == customer_id)
        .filter(Favorite.product_id == product_id)
        .first()
    )
    
    if not favorite:
        raise FavoriteNotFoundError(product_id)
    
    product_data = await get_product_by_id(product_id)
    
    if not product_data:
        raise ProductNotFoundError(product_id)

    return FavoriteReponse(
                product_id=product_data.get("id"),
                customer_id=customer_id,
                title=product_data.get("title"),
                price=product_data.get("price"),
                image=product_data.get("image"),
                rating=product_data.get("rating"),
            )

async def get_favorites(db: Session, customer_id: UUID) -> List[FavoriteReponse]:
    favorites = db.query(Favorite).filter(Favorite.customer_id == customer_id).all()

    tasks = []
    for favorite in favorites:
        tasks.append(get_product_by_id(favorite.product_id))
    
    products_data = await asyncio.gather(*tasks)
    
    response = []
    for favorite, product_data in zip(favorites, products_data):
        if product_data:
            response.append(
                FavoriteReponse(
                    product_id=product_data.get("id"),
                    customer_id=customer_id,
                    title=product_data.get("title"),
                    price=product_data.get("price"),
                    image=product_data.get("image"),
                    rating=product_data.get("rating"),
                )
            )
    
    return response

def remove_product_from_favorites(db: Session, product_id: int, customer_id: UUID) -> None:
    favorite = (
        db.query(Favorite)
        .filter(Favorite.customer_id == customer_id)
        .filter(Favorite.product_id == product_id)
        .first()
    )

    if not favorite:
        raise FavoriteNotFoundError(product_id)

    db.delete(favorite)
    db.commit()