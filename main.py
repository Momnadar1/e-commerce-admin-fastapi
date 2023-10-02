from fastapi import FastAPI
from routes.route import *

app = FastAPI()

@app.get("/ping", tags=["Health"])
async def health():
    """
    Health Check
    """
    return {"message": "pong"}

app.include_router(product_router, prefix="/api/v1", tags=["Product"])

app.include_router(sale_router, prefix="/api/v1", tags=["Sale"])
