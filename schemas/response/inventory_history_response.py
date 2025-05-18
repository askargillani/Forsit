from pydantic import BaseModel

class InventoryHistoryResponse(BaseModel):
    date: str
    change: int
    new_quantity: int
