from pydantic import BaseModel
from typing import Optional

class InventoryListResponse(BaseModel):
    product: str
    quantity: int
    updated_at: Optional[str]
