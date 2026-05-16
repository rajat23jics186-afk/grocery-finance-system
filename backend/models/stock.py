"""Stock history model."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from backend.database import Base


class StockHistory(Base):
    """Stock history tracking model."""
    
    __tablename__ = "stock_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity_change = Column(Integer, nullable=False)
    transaction_type = Column(String(20), default="sale")  # purchase, sale, return, adjustment
    reference_order_id = Column(Integer, ForeignKey("orders.id"))
    notes = Column(String(500))
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<StockHistory {self.id}>"
