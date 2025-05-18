from pydantic import BaseModel  

class RevenueResponse(BaseModel):
    revenue1: float
    revenue2: float
    change: float
