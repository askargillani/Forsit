from pydantic import BaseModel

class ByCategoryResponse(BaseModel):
    category: str
    revenue: float
