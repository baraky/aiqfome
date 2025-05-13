from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Rating(BaseModel):
    rate: float
    count: int

class Product(BaseModel):
    product_id: int
    title: str
    image: str
    price: float
    rating: Optional[Rating]