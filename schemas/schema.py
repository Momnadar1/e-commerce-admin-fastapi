from pydantic import BaseModel

class Product(BaseModel):
    # __tablename__ = "product"

    name: str
    description: str
    price: float
    category: str
    quantity_in_stock: int