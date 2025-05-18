from sqlalchemy import Column, Integer, String
from models.base import Base

class Category(Base):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)