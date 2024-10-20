from .models import Product, Purchase
from .database import SessionLocal

def get_product_by_code(code: str):
    db = SessionLocal()
    return db.query(Product).filter(Product.code == code).first()

def create_purchase(purchase_list: list):
    db = SessionLocal()
    total = sum([item['price'] for item in purchase_list])
    purchase = Purchase(total=total)
    db.add(purchase)
    db.commit()
    return total
