from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from models.base import Base
import datetime

class Inventory(Base):
    __tablename__ = "Inventory"
    product_id = Column(Integer, ForeignKey("Products.id"), primary_key=True)
    quantity = Column(Integer, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)