# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, database

app = FastAPI()

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

# Create Product Schema for Request/Response
from pydantic import BaseModel

class ProductCreate(BaseModel):
    product_code: str
    product_name: str
    product_price: float

class ProductUpdate(BaseModel):
    product_name: str
    product_price: float

@app.post("/products/", response_model=ProductCreate)
def create_product(product: ProductCreate, db: Session = Depends(database.get_db)):
    db_product = models.Product(
        product_code=product.product_code,
        product_name=product.product_name,
        product_price=product.product_price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_code}", response_model=ProductCreate)
def read_product(product_code: str, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.product_code == product_code).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_code}", response_model=ProductCreate)
def update_product(product_code: str, product: ProductUpdate, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.product_code == product_code).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_product.product_name = product.product_name
    db_product.product_price = product.product_price
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_code}", response_model=str)
def delete_product(product_code: str, db: Session = Depends(database.get_db)):
    db_product = db.query(models.Product).filter(models.Product.product_code == product_code).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return "Product deleted successfully"
