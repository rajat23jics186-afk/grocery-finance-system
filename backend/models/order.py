"""Order models."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.database import Base


class Order(Base):
    """Order model."""
    
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    order_date = Column(DateTime, default=func.now())
    total_amount = Column(Float, nullable=False)
    payment_status = Column(String(20), default="pending")  # pending, completed, failed, partial
    order_status = Column(String(20), default="pending")  # pending, confirmed, shipped, delivered, cancelled
    shipping_address = Column(String(255))
    expected_delivery_date = Column(DateTime)
    actual_delivery_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order {self.id}>"


class OrderItem(Base):
    """Order line item model."""
    
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now())

    order = relationship("Order", back_populates="items")

    def __repr__(self):
        return f"<OrderItem {self.id}>"
