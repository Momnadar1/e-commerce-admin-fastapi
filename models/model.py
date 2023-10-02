from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base  = declarative_base()

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement = True, index=True)
    name = Column(String(255))
    description = Column(String(255))
    price = Column(Float)
    category = Column(String(255))
    quantity_in_stock = Column(Integer)