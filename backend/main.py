from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from pydantic import BaseModel
from backend.database import SessionLocal, engine
from backend.models import Product, Purchase, PurchaseDetail
from dotenv import load_dotenv
import os

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
engine = create_engine(DATABASE_URL)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    


# 商品検索エンドポイント
@app.get("/api/products/{code}")
def read_product(code: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.code == code).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"id": product.id, "code": product.code, "name": product.name, "price": product.price}

class PurchaseItem(BaseModel):
    product_id: int
    quantity: int

class PurchaseRequest(BaseModel):
    purchase_list: list[PurchaseItem]

@app.post("/api/purchase")
def create_purchase(request: PurchaseRequest, db: Session = Depends(get_db)):
    total_amount = 0
    purchase = Purchase(total_amount = 0) #初期値を0とする
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    for item in request.purchase_list:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        
        purchase_detail = PurchaseDetail(
            purchase_id=purchase.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price * item.quantity
        )
        total_amount += product.price * item.quantity
        db.add(purchase_detail)
    
    # 合計金額を更新して保存
    purchase.total_amount = total_amount
    db.commit()

    return {"message": "Purchase completed", "total_amount": total_amount}