from pydantic import BaseModel

class InventoryUpdateResponse(BaseModel):
    product_name: str
    new_quantity: int
    status: str
