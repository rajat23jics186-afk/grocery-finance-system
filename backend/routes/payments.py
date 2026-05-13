"""Payment routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import get_db
from backend.models.payment import Payment
from backend.models.order import Order

router = APIRouter(prefix="/api/payments", tags=["Payments"])


class PaymentCreate(BaseModel):
    """Payment creation schema."""
    order_id: int
    customer_id: int
    amount: float
    payment_method: str = "cash"


@router.post("/", response_model=dict)
def create_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    """Record a payment."""
    order = db.query(Order).filter(Order.id == payment_data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if payment_data.amount > order.total_amount:
        raise HTTPException(status_code=400, detail="Payment amount exceeds order total")
    
    db_payment = Payment(**payment_data.model_dump())
    db_payment.status = "completed"
    db.add(db_payment)
    
    # Update order payment status
    if payment_data.amount == order.total_amount:
        order.payment_status = "completed"
    else:
        order.payment_status = "partial"
    
    db.commit()
    db.refresh(db_payment)
    return {"id": db_payment.id, "status": "completed", "message": "Payment recorded"}


@router.get("/")
def list_payments(order_id: int = None, customer_id: int = None, db: Session = Depends(get_db)):
    """List payments with optional filters."""
    query = db.query(Payment)
    if order_id:
        query = query.filter(Payment.order_id == order_id)
    if customer_id:
        query = query.filter(Payment.customer_id == customer_id)
    return query.all()


@router.get("/{payment_id}")
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get single payment by ID."""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
