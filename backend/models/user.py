"""User model."""

from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, func
from backend.database import Base


class User(Base):
    """User model for Owner and Customers."""
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="retail")  # owner, retail, wholesale
    phone = Column(String(20))
    address = Column(String(255))
    city = Column(String(50))
    state = Column(String(50))
    pincode = Column(String(10))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    credit_limit = Column(Float, default=0.0)
    credit_used = Column(Float, default=0.0)

    def __repr__(self):
        return f"<User {self.username}>"
