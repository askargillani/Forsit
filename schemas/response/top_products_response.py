from pydantic import BaseModel

class TopProductResponse(BaseModel):
    product_name: str
    total_quantity: int
