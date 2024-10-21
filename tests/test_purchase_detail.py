from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from backend.main import app, get_db
from backend.models import Product, PurchaseDetail, Purchase
from backend.database import SessionLocal

client = TestClient(app)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_create_purchase_detail():
    # 商品を事前に作成
    response = client.post("/api/products/", json={
        "code": "4900000000003",
        "name": "Sample Product",
        "price": 1000
    })
    assert response.status_code == 200
    product_id = response.json()["id"]

    # 購入を作成して、購入詳細を追加
    response = client.post("/api/purchase", json={
        "purchase_list": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    })
    assert response.status_code == 200
    assert response.json()["total_amount"] == 2000

    # DBを直接チェックして購入詳細を確認
    db: Session = SessionLocal()
    purchase_details = db.query(PurchaseDetail).all()
    assert len(purchase_details) == 1
    assert purchase_details[0].product_id == product_id
    assert purchase_details[0].quantity == 2
    assert purchase_details[0].price == 2000

    db.close()
