from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(13), unique=True, index=True)
    name = Column(String(50))
    price = Column(Float)

class Purchase(Base):
    __tablename__ = 'purchases'
    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Float)

    details = relationship("PurchaseDetail", back_populates="purchase")

class PurchaseDetail(Base):
    __tablename__ = "purchase_details"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey('purchases.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    price = Column(Float)

    # 関連するエンティティを定義（任意）
    purchase = relationship("Purchase", back_populates="details")
    product = relationship("Product")