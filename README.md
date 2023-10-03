# E-commerce Admin API

This is a FastAPI-based back-end API for an e-commerce admin dashboard. It provides functionalities for managing sales data, analyzing revenue, and registering new products.

## Features

1. **Sales Status:**
   - Endpoints to retrieve, filter, and analyze sales data.
   - Endpoints to analyze revenue on a daily, weekly, monthly, and annual basis.
   - Ability to compare revenue across different periods and categories.
   - Provide sales data by date range, product, and category.

2. **Product Management:**
   - Endpoints todo CRUD operations.

## Technical Stack

- FastAPI for building the API.
- SQLAlchemy for database management.
- MySQL for the relational database.
- Python for coding.

## Database Setup

1. Create a MySQL database for the project.
2. Define the database connection URL in the FastAPI application.
3. Define the database schema with tables for products, and sales.

## API Endpoints

- **Sales:**
   - Retrieve sales data by date range, year, and month.
   - Analyze revenue for various periods.

- **Products:**
   - Register new products.

## Getting Started

1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`.
3. Run the FastAPI application: `uvicorn main:app --reload`.
4. Access the API at `http://localhost:8000`.
5. Use Postman or any other REST client tool of your choice to test out endpoints.

## 1. Clone the repository
```shell
git clone git@github.com:Momnadar1/e-commerce-admin-fastapi.git
```
## 2. Virtual environment
Create and activate virtual environment:
```shell
cd e-commerce-admin-fastapi
python -m venv venv
source venv/Scripts/activate
```

## 3. Create a `.env` file
```shell
pip install -r requirements.txt
```

## 4. Database population
Note: create the databases and populate sample data into the database tables.
```shell
cd scripe__db_sample_data_population
cd ..
```
Foot-Note: Run each cell and populate data with the sequence of cells.

## 5. Start the Application

```shell
uvicorn main:app --reload
```
The API will be accessible at [http://localhost:8000](http://localhost:8000).

## 6. List of endpoints (./routes/)

### Methods Allowed: GET
[http://localhost:8000/sales/](http://localhost:8000/sales/)

### Methods Allowed: GET
[http://localhost:8000/sales/daily](http://localhost:8000/sales/daily)

### Methods Allowed: GET
[http://localhost:8000/sales/weekly](http://localhost:8000/sales/weekly)

### Methods Allowed: GET
[http://localhost:8000/sales/monthly](http://localhost:8000/sales/monthly)

### Methods Allowed: GET
[http://localhost:8000/sales/annual](http://localhost:8000/sales/annual)

### Methods Allowed: GET, PUT, POST, DELETE
[http://localhost:8000/products/](http://localhost:8000/products/) 

## 7. API Documentation
Find swagger docs at [http://127.0.1:8000/docs/](http://127.0.0.1:8000/docs).

To access the Swagger documentation and test the endpoints, visit [http://localhost:8000/docs](http://localhost:8000/docs) and [http://localhost:8000/redoc](http://localhost:8000/redoc) in your web browser.
