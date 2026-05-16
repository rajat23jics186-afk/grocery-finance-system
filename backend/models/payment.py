"""Payment model."""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from backend.database import Base


class Payment(Base):
    """Payment model."""
    
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(20), default="cash")  # cash, credit_card, debit_card, upi, bank_transfer
    payment_date = Column(DateTime, default=func.now())
    transaction_id = Column(String(100), unique=True)
    status = Column(String(20), default="pending")  # pending, completed, failed
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Payment {self.id}>"
