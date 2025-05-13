from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.db.core import Base

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

def __repr__(self) -> str:
    return f"Customer(name='{self.name}', email='{self.email}')"