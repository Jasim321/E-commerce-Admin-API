from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from app.db import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_date = Column(DateTime)
    sale_quantity = Column(Integer)
    sale_price = Column(Float)
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="sales")
