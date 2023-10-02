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
    
    
class Sale(Base):
    __tablename__ = "sale"

    invoice_id = Column(String(255), primary_key=True)
    branch = Column(String(255))
    city = Column(String(255))
    customer_type = Column(String(255))
    gender = Column(String(255))
    product_line = Column(String(100))
    unit_price = Column(Float)
    quantity = Column(Integer)
    tax_pct = Column(Float(6, 4))
    total = Column(Float(12, 4))
    date = Column(DateTime)
    time = Column(DateTime)
    payment = Column(String(255))
    cogs = Column(Float(10, 2))
    gross_margin_pct = Column(Float(11, 9))
    gross_income = Column(Float(12, 4))
    rating = Column(Float(2, 1))
    product_id = Column(Integer, ForeignKey("product.id"))
