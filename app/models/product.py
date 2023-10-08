from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    category_id = Column(Integer, ForeignKey("categories.id"))

    sales = relationship("Sale", back_populates="product")
    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product")
