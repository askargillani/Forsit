from pydantic import BaseModel

class LowStockResponse(BaseModel):
    product: str
    quantity: int
