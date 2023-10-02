from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, Float, DateTime, Time, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from datetime import datetime, timedelta, date
from sqlalchemy import and_, func
from dateutil.rrule import rrule, DAILY



# Initialize FastAPI
app = FastAPI()

host = "localhost"
user = "root"
password = "root"
database_name = "walmart"
port = 3306

# Define the database connection URL
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the database model
Base = declarative_base()

class Sale(Base):
    __tablename__ = "sale"

    invoice_id = Column(String(255), primary_key=True)
    branch = Column(String(255))
    city = Column(String(255))
    customer_type = Column(String(255))
    gender = Column(String(255))
    productline = Column(String(100))
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
    productid = Column(Integer, ForeignKey("product.id"))

# API endpoints
# class SaleRequest(BaseModel):
#     start_date: str
#     end_date: str
#     productline: str = None

@app.get("/sales/")
async def get_sales(
    start_date: date,
    end_date: date,
):
    # Create a database session
    session = SessionLocal()

    # Build the query to filter sales data
    query = session.query(Sale).filter(func.date(Sale.date).between(start_date, end_date))

    # Execute the query and retrieve sales data
    sales = query.all()

    # Close the database session
    session.close()

    return {'sales':sales}

@app.get("/revenue/daily")
async def daily_revenue(start_date: date, end_date: date):
     # Calculate the start and end of the week
    total_revenue = []
    session = SessionLocal()
    print(list(rrule(freq=DAILY, dtstart=start_date, until=end_date)))
    for date in list(rrule(freq=DAILY, dtstart=start_date, until=end_date)):
        result = session.query(func.sum(Sale.total)).filter(func.date(Sale.date) == date.date())
        revenue = result.one()
        total_revenue.append({'revenue':[(revenue[0]) if revenue[0] else 0], 'date':date.date()})
    session.close()
    return {"daily_revenue": total_revenue}

@app.get("/revenue/weekly")
async def weekly_revenue(year: int, month: int):
    # Calculate the start and end of the week
    total_revenue = []
    session = SessionLocal()
    for week_number in range(1, 5):
        result = session.query(func.sum(Sale.total)).filter(func.year(Sale.date) == year,
                                                            func.month(Sale.date) == month,
                                                            func.weekday(Sale.date) == week_number)
        revenue = result.one()
        total_revenue.append({'revenue':[(revenue[0]) if revenue[0] else 0], 'year':year,'month':month, 'week_number':week_number})
    session.close()
    return {"weekly_revenue": total_revenue}

@app.get("/revenue/monthly")
async def monthly_revenue(year: int):
    total_revenue = []
    session = SessionLocal()
    for month in range(1, 13):
        result = session.query(func.sum(Sale.total)).filter(func.year(Sale.date) == year,
                                                            func.month(Sale.date) == month)
        revenue = result.one()
        total_revenue.append({'revenue':[(revenue[0]) if revenue[0] else 0], 'year':year,'month':month})
    session.close()
    return {"monthly_revenue": total_revenue}

@app.get("/revenue/annual")
async def annual_revenue(start_year: int, end_year: int):
    total_revenue = []
    session = SessionLocal()
    for year in range(start_year, end_year+1):
        result = session.query(func.sum(Sale.total)).filter(func.year(Sale.date) == year)
        revenue = result.one()
        total_revenue.append({'revenue':[(revenue[0]) if revenue[0] else 0], 'year':year})
    session.close()
    return {"annual_revenue": total_revenue}

from models.model import Product as ProductModel
from schemas.schema import Product as ProductSchema


@app.post("/products/")
def create_product(product: ProductSchema):
    session = SessionLocal()
    new_product = ProductModel(name=product.name, description=product.description, price=product.price, 
                               category=product.category, quantity_in_stock=product.quantity_in_stock)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@app.get("/products/{product_id}", response_model=ProductSchema)
def read_product(product_id: int):
    session = SessionLocal()
    product = session.query(ProductModel).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductSchema):
    session = SessionLocal()
    existing_product = session.query(ProductModel).get(product_id)
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = product.model_dump()
    for key, value in product_data.items():
        setattr(existing_product, key, value)

    session.commit()
    session.refresh(existing_product)
    return existing_product

@app.delete("/products/{product_id}", response_model=dict)
def delete_product(product_id: int):
    session = SessionLocal()
    product = session.query(ProductModel).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    session.delete(product)
    session.commit()
    return {"message": "Product deleted"}


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)