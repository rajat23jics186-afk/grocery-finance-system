"""Product model."""

from sqlalchemy import Column, Integer, String, Float, DateTime, func
from backend.database import Base


class Product(Base):
    """Product model."""
    
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(50), index=True, nullable=False)
    description = Column(String(500))
    retail_price = Column(Float, nullable=False)
    wholesale_price = Column(Float, nullable=False)
    quantity_in_stock = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    supplier = Column(String(100))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Product {self.name}>"
