from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
    __tablename__ = "商品マスタ"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_code = Column(String(50), unique=True, index=True)
    product_name = Column(String(100))
    product_price = Column(Float)