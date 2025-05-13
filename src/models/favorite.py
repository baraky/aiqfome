from pydantic import BaseModel
from uuid import UUID
from src.models.product import Product

class FavoriteCreate(BaseModel):
    customer_id: UUID
    product_id: int
    
class FavoriteReponse(Product):
    customer_id: UUID
