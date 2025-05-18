from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from models.base import Base
import datetime

class Product(Base):
    __tablename__ = "Products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("Categories.id"))
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)