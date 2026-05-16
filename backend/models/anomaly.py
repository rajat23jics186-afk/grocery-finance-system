"""Anomaly detection model."""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from backend.database import Base


class Anomaly(Base):
    """Anomaly detection model for fraud and unusual patterns."""
    
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    anomaly_type = Column(String(20), nullable=False)  # fraud, outlier, unusual_pattern
    customer_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    severity = Column(String(20), default="low")  # low, medium, high
    description = Column(String(500))
    detected_at = Column(DateTime, default=func.now())
    is_resolved = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Anomaly {self.id}>"
