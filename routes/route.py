from datetime import date
from sqlalchemy import func
from models.model import Sale as SaleModel
from schemas.schema import Sale as SaleSchema
from models.model import Product as ProductModel
from schemas.schema import Product as ProductSchema
from dateutil.rrule import rrule, DAILY
from fastapi import APIRouter, HTTPException, Depends
from database.db import *

product_router = APIRouter(
    prefix="/products",
    responses={404: {"description": "Not found"}},
)

sale_router = APIRouter(
    prefix="/sales",
    responses={404: {"description": "Not found"}},
)


@sale_router.get("/", response_model=SaleSchema)
async def get_sales(
    start_date: date,
    end_date: date,
    session = Depends(get_db)
):
    # Build the query to filter sales data
    query = session.query(SaleModel).filter(func.date(SaleModel.date).between(start_date, end_date))

    # Execute the query and retrieve sales data
    sales = query.all()

    # Close the database session
    session.close()

    return {'sales':sales}

@sale_router.get("/daily")
async def daily_revenue(start_date: date, end_date: date, session = Depends(get_db)):
     # Calculate the start and end of the week
    total_revenue = []
    # session = SessionLocal()
    print(list(rrule(freq=DAILY, dtstart=start_date, until=end_date)))
    for date in list(rrule(freq=DAILY, dtstart=start_date, until=end_date)):
        result = session.query(func.sum(SaleModel.total)).filter(func.date(SaleModel.date) == date.date())
        revenue = result.one()
        total_revenue.append({'revenue':[(revenue[0]) if revenue[0] else 0], 'date':date.date()})
    session.close()
    return {"daily_revenue": total_revenue}

@sale_router.get("/weekly")
async def weekly_revenue(year: int, month: int, session = Depends(get_db)):
    # Calculate the start and end of the week
    total_revenue = []
    # session = SessionLocal()
    for week_number in range(1, 5):
        result = session.query(func.sum(SaleModel.total)).filter(func.year(SaleModel.date) == year,
                                                            func.month(SaleModel.date) == month,
                                                            func.weekday(SaleModel.date) == week_number)
        revenue = result.one()
        total_revenue.append({'revenue':[(revenue[0]) if revenue[0] else 0], 'year':year,'month':month, 'week_number':week_number})
    session.close()
    return {"weekly_revenue": total_revenue}

@sale_router.get("/monthly")
async def monthly_revenue(year: int, session = Depends(get_db)):
    total_revenue = []
    # session = SessionLocal()
    for month in range(1, 13):
        result = session.query(func.sum(SaleModel.total)).filter(func.year(SaleModel.date) == year,
                                                            func.month(SaleModel.date) == month)
        revenue = result.one()
        total_revenue.append({'revenue':[(revenue[0]) if revenue[0] else 0], 'year':year,'month':month})
    session.close()
    return {"monthly_revenue": total_revenue}

@sale_router.get("/annual")
async def annual_revenue(start_year: int, end_year: int, session = Depends(get_db)):
    total_revenue = []
    # session = SessionLocal()
    for year in range(start_year, end_year+1):
        result = session.query(func.sum(SaleModel.total)).filter(func.year(SaleModel.date) == year)
        revenue = result.one()
        total_revenue.append({'revenue':[(revenue[0]) if revenue[0] else 0], 'year':year})
    session.close()
    return {"annual_revenue": total_revenue}

@product_router.post("/create/")
def create_product(product: ProductSchema, session = Depends(get_db)):
    """
    Products
    """
    # session = SessionLocal()
    new_product = ProductModel(name=product.name, description=product.description, price=product.price, 
                               category=product.category, quantity_in_stock=product.quantity_in_stock)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@product_router.get("/{product_id}", response_model=ProductSchema)
def read_product(product_id: int, session = Depends(get_db)):
    # session = SessionLocal()
    product = session.query(ProductModel).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@product_router.put("/{product_id}")
def update_product(product_id: int, product: ProductSchema, session = Depends(get_db)):
    # session = SessionLocal()
    existing_product = session.query(ProductModel).get(product_id)
    if existing_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    product_data = product.model_dump()
    for key, value in product_data.items():
        setattr(existing_product, key, value)

    session.commit()
    session.refresh(existing_product)
    return existing_product

@product_router.delete("/{product_id}", response_model=dict, )
def delete_product(product_id: int, session = Depends(get_db)):
    # session = SessionLocal()
    product = session.query(ProductModel).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    session.delete(product)
    session.commit()
    return {"message": "Product deleted"}
