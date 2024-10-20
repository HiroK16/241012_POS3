from fastapi import FastAPI, HTTPException
from backend.models import Product, Purchase
from backend.crud import get_product_by_code, create_purchase
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()

db_config = {
    'user': 'root',
    'password': os.getenv("DATABASE_PASSWORD"),  # MySQLのパスワードに合わせて変更
    'host': 'localhost',
    'database': 'pos_app'
}

@app.get("/api/products/{code}")
async def read_product(code: str):
    product = get_product_by_code(code)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/purchase")
async def purchase_items(purchase_list: list):
    total = create_purchase(purchase_list)
    return {"total": total}
