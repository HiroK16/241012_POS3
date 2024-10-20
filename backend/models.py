from sqlalchemy import Column, Integer, String, Float
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
    total = Column(Float)
