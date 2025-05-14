from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from src.entities.customer import Customer
from src.models.customer import CustomerReponse, RegisterCustomerRequest
from src.auth.service import get_password_hash
from src.exceptions import *

def get_customer_by_id(db: Session, customer_id: UUID) -> CustomerReponse:
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise CustomerNotFoundError(customer_id)
    return customer

def register_customer(db: Session, register_customer_request: RegisterCustomerRequest) -> None:
    existing_customer = db.query(Customer).filter(
        Customer.email == register_customer_request.email
    ).first()
    
    if existing_customer:
        raise UniqueEmailError(register_customer_request.email)
    
    new_customer = Customer(
        id=uuid4(),
        email=register_customer_request.email,
        name=register_customer_request.name,
        password=get_password_hash(register_customer_request.password)
    )
    db.add(new_customer)
    db.commit()

def update_customer(db: Session, customer_id: UUID, costumer_update: RegisterCustomerRequest) -> Customer:
    customer_data = costumer_update.model_dump(exclude_unset=True)
    
    existing_customer = db.query(Customer).filter(
        Customer.email == costumer_update.email
    ).first()
    
    if existing_customer:
        raise UniqueEmailError(costumer_update.email)

    db.query(Customer).filter(Customer.id == customer_id).update(customer_data)
    db.commit()
    return get_customer_by_id(db, customer_id)

def delete_customer(db: Session, customer_id: UUID) -> None:
    customer = get_customer_by_id(db, customer_id)
    db.delete(customer)
    db.commit()