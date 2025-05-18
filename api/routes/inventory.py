from fastapi import APIRouter, Depends, Query, Body
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from schemas.request.add_product_request import AddProductRequest
from services.service import Service
from repository.database import SessionLocal
from schemas.request.inventory_update_request import InventoryUpdateRequest
from schemas.response.inventory_update_response import InventoryUpdateResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/history")
def get_inventory_history(
    product_name: str = Query(..., description="Product Name"),
    startDate: Optional[datetime] = None,
    endDate: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    service = Service(db)
    history = service.get_inventory_history(product_name, startDate, endDate)
    return {"history": history}

@router.post("/update", response_model=InventoryUpdateResponse)
def update_inventory(
    body: InventoryUpdateRequest = Body(...),
    db: Session = Depends(get_db)
):
    service = Service(db)
    result = service.update_inventory(
        product_name=body.product_name,
        quantity_change=body.quantity_change
    )
    return result

@router.get("")
def get_inventory(
    product_name: str = Query(None, description="Product Name"),
    db: Session = Depends(get_db)
):
    service = Service(db)
    inventory = service.get_inventory(product_name)
    return {"inventory": inventory}

@router.get("/low-stock")
def get_low_stock(
    threshold: int = Query(..., description="Stock threshold"),
    db: Session = Depends(get_db)
):
    service = Service(db)
    low_stock = service.get_low_stock(threshold)
    return {"low_stock": low_stock}

@router.post("/add-product")
def add_product(
    body: AddProductRequest = Body(...),
    db: Session = Depends(get_db)
):
    service = Service(db)
    result = service.add_product(body.product_name, body.quantity, body.category, body.price)
    return {"result": result}
