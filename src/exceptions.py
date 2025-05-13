from fastapi import HTTPException

class CustomerNotFoundError(HTTPException):
    def __init__(self, customer_id=None):
        message = "Customer not found" if customer_id is None else f"Customer with id {customer_id} not found"
        super().__init__(status_code=404, detail=message)

class FavoriteCreationError(HTTPException):
    def __init__(self, error: str):
        super().__init__(status_code=500, detail=f"Failed to add product to favorite list: {error}")

class FavoriteAlreadyExistsError(HTTPException):
    def __init__(self, product_id=None):
        super().__init__(status_code=500, detail=f"Product with id {product_id} is already in favorite list")

class FavoriteNotFoundError(HTTPException):
    def __init__(self, product_id=None):
        message = "Favorite product not found" if product_id is None else f"Favorite product with id {product_id} not found"
        super().__init__(status_code=404, detail=message)

class ProductNotFoundError(HTTPException):
    def __init__(self, product_id=None):
        message = "Product not found" if product_id is None else f"Product with id {product_id} not found"
        super().__init__(status_code=404, detail=message)

class AuthenticationError(HTTPException):
    def __init__(self, message: str = "Could not validate customer"):
        super().__init__(status_code=401, detail=message)