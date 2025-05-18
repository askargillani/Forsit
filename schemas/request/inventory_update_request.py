from pydantic import BaseModel

class InventoryUpdateRequest(BaseModel):
    product_name: str
    quantity_change: int
