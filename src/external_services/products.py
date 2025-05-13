import httpx
from dotenv import load_dotenv
import os

load_dotenv()

FAKESTORE_API_URL = os.getenv("FAKESTORE_API_URL")

async def get_product_by_id(product_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(FAKESTORE_API_URL.format(id=product_id))
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            return None