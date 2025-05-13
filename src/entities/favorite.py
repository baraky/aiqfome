from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from src.db.core import Base

class Favorite(Base):
    __tablename__ = 'favorites'

    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'), primary_key=True)
    product_id = Column(Integer, primary_key=True)

def __repr__(self) -> str:
    return f"Favorite(customer_id='{self.customer_id}', product_id='{self.product_id}')"