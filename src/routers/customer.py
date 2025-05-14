from fastapi import APIRouter
from starlette import status
from src.models.customer import CustomerReponse, RegisterCustomerRequest
from src.db.core import DbSession
from src.auth.service import CurrentCustomer
import src.api.customer as service

router = APIRouter(
    prefix='/customers',
    tags=['Customers']
)
@router.post("/", response_model=CustomerReponse, status_code=status.HTTP_201_CREATED)
async def register_customer(db: DbSession,
                            register_customer_request: RegisterCustomerRequest):
    return service.register_customer(db, register_customer_request)

@router.put("/me", response_model=CustomerReponse)
async def update_current_customer(db: DbSession,
                            current_customer: CurrentCustomer,
                            update_customer_request: RegisterCustomerRequest):
    customer_id = current_customer.get_uuid()
    return service.update_customer(db, customer_id, update_customer_request)

@router.get("/me", response_model=CustomerReponse)
async def get_current_customer(db: DbSession, current_customer: CurrentCustomer):
    return service.get_customer_by_id(db, current_customer.get_uuid())

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_customer(db: DbSession, current_customer: CurrentCustomer):
    service.delete_customer(db, current_customer.get_uuid())