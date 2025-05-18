from sqlalchemy import Column, Integer, DateTime, ForeignKey
from models.base import Base
import datetime

class InventoryHistory(Base):
    __tablename__ = "InventoryHistory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("Products.id"))
    quantity_change = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    changed_at = Column(DateTime, default=datetime.datetime.utcnow)