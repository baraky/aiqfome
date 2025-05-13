from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from src.entities.customer import Customer
from src.models.customer import CustomerReponse, RegisterCustomerRequest
from src.auth.service import get_password_hash
from src.exceptions import CustomerNotFoundError

def get_customer_by_id(db: Session, customer_id: UUID) -> CustomerReponse:
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise CustomerNotFoundError(customer_id)
    return customer

def register_customer(db: Session, register_customer_request: RegisterCustomerRequest) -> None:
    try:
        create_customer_model = Customer(
            id = uuid4(),
            email = register_customer_request.email,
            name = register_customer_request.name,
            password = get_password_hash(register_customer_request.password)
        )
        db.add(create_customer_model)
        db.commit()
    except Exception as e:
        raise

def update_customer(db: Session, customer_id: UUID, costumer_update: RegisterCustomerRequest) -> Customer:
    customer_data = costumer_update.model_dump(exclude_unset=True)
    db.query(Customer).filter(Customer.id == customer_id).update(customer_data)
    db.commit()
    return get_customer_by_id(db, customer_id)

def delete_customer(db: Session, customer_id: UUID) -> None:
    customer = get_customer_by_id(db, customer_id)
    db.delete(customer)
    db.commit()