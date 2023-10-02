from pydantic import BaseModel
from datetime import datetime

class Product(BaseModel):
    # __tablename__ = "product"

    name: str
    description: str
    price: float
    category: str
    quantity_in_stock: int
    
class Sale(BaseModel):
    # __tablename__ = "sale"

    invoice_id: str
    branch: str
    city: str
    customer_type: str
    gender: str
    product_line: str
    unit_price: float
    quantity: int 
    tax_pct: float
    total: float
    date: datetime
    time: datetime
    payment: str
    cogs: float
    gross_margin_pct: float
    gross_income: float
    rating: float
    product_id: int 