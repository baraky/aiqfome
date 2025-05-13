from fastapi import FastAPI
from src.routers.auth import router as auth_router
from src.routers.customer import router as customer_router
from src.routers.favorite import router as favorite_router
from src.db.core import Base, engine

app = FastAPI()

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(favorite_router)

Base.metadata.create_all(bind=engine)