from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from models.base import Base
import datetime

class Sale(Base):
    __tablename__ = "Sales"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("Products.id"))
    quantity = Column(Integer, nullable=False)
    sale_date = Column(DateTime, default=datetime.datetime.utcnow)