from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from services.service import Service
from repository.database import engine, SessionLocal

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/revenue")
def get_revenue(
    startDate: Optional[datetime] = None,
    endDate: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    service = Service(db)
    revenue = service.get_revenue_by_period(startDate, endDate)
    return {"revenue": revenue}

@router.get("/revenue-comparison")
def get_revenue_comparison(
    startDate1: Optional[datetime] = None,
    endDate1: Optional[datetime] = None,
    startDate2: Optional[datetime] = None,
    endDate2: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    service = Service(db)
    comparison = service.get_revenue_comparison(startDate1, endDate1, startDate2, endDate2)
    return comparison    

@router.get("/top-products")
def get_top_products(
    startDate: Optional[datetime] = None,
    endDate: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    service = Service(db)
    top_products = service.get_top_products(startDate, endDate)
    return {"top_products": top_products}

@router.get("/by-category")
def get_by_category(
    startDate: Optional[datetime] = None,
    endDate: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    service = Service(db)
    result = service.get_revenue_by_category(startDate, endDate)
    return {"by_category": result}



