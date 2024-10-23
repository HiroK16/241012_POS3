from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from pydantic import BaseModel
from backend.database import SessionLocal, engine
from backend.models import Product, Purchase, PurchaseDetail
from dotenv import load_dotenv
import os
import logging

#ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

load_dotenv()

db_password = os.getenv("DATABASE_PASSWORD")

print(f"Database password is: {db_password}")

db_config = {
    'user': 'root',
    'password': db_password,  # MySQLのパスワードに合わせて変更
    'host': 'localhost',
    'database': 'pos_app'
}

# 接続文字列の作成
DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

# データベースエンジンの作成
try:
    engine = create_engine(DATABASE_URL)
    logger.info("Database connection successful")
except Exception as e:
    logger.error(f"Database connection failed: {e}")    

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    try:
        db = SessionLocal()
        logger.info("Session started")
        yield db
    finally:
        db.close()    
        logger.info("Session closed")


# 商品検索エンドポイント
@app.get("/api/products/{code}")
def read_product(code: str, db: Session = Depends(get_db)):
    logger.info(f"Received request to read product with code: {code}")
    product = db.query(Product).filter(Product.code == code).first()
    if product is None:
        logger.warning(f"Product not found: {code}")
        raise HTTPException(status_code=404, detail="Product not found")
    logger.info(f"Product found: {product}")
    return {"id": product.id, "code": product.code, "name": product.name, "price": product.price}

class PurchaseItem(BaseModel):
    product_id: int
    quantity: int

class PurchaseRequest(BaseModel):
    purchase_list: list[PurchaseItem]

class ProductCreate(BaseModel):
    code: str
    name: str
    price: int    

@app.post("/api/products")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(code=product.code, name=product.name, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.post("/api/purchase")
def create_purchase(request: PurchaseRequest, db: Session = Depends(get_db)):
    logger.info(f"Received purchase request: {request}")
    total_amount = 0
    try:
        purchase = Purchase(total_amount = 0) #初期値を0とする
        db.add(purchase)
        db.commit()
        db.refresh(purchase)
        logger.info(f"Created purchase with ID: {purchase.id}")

        for item in request.purchase_list:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product is None:
                logger.warning(f"Product not found for ID: {item.product_id}")
                raise HTTPException(status_code=404, detail="Product not found")
        
        purchase_detail = PurchaseDetail(
            purchase_id=purchase.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price * item.quantity
        )
        total_amount += product.price * item.quantity
        db.add(purchase_detail)
        logger.info(f"Added purchase detail: {purchase_detail}")
    
        # 合計金額を更新して保存
        purchase.total_amount = total_amount
        db.commit()
        logger.info(f"Purchase completed with total amount: {total_amount}")
    except Exception as e:
        logger.error(f"Error during purchase creation: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"message": "Purchase completed", "total_amount": total_amount}