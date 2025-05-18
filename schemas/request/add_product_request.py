from pydantic import BaseModel

class AddProductRequest(BaseModel):
    product_name: str
    quantity: int
    price: float
    category: str

