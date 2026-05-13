"""Order routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from backend.database import get_db
from backend.models.order import Order, OrderItem
from backend.models.product import Product

router = APIRouter(prefix="/api/orders", tags=["Orders"])


class OrderItemCreate(BaseModel):
    """Order item creation schema."""
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    """Order creation schema."""
    customer_id: int
    items: List[OrderItemCreate]
    shipping_address: str


@router.post("/", response_model=dict)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order."""
    # Calculate total
    total_amount = 0
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        if product.quantity_in_stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        
        total_amount += product.retail_price * item.quantity
    
    # Create order
    db_order = Order(
        customer_id=order_data.customer_id,
        total_amount=total_amount,
        shipping_address=order_data.shipping_address,
    )
    db.add(db_order)
    db.flush()
    
    # Add order items
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        order_item = OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.retail_price,
            subtotal=product.retail_price * item.quantity,
        )
        db.add(order_item)
        # Update stock
        product.quantity_in_stock -= item.quantity
    
    db.commit()
    db.refresh(db_order)
    return {"id": db_order.id, "total_amount": db_order.total_amount, "message": "Order created"}


@router.get("/")
def list_orders(customer_id: int = None, status: str = None, db: Session = Depends(get_db)):
    """List orders with optional filters."""
    query = db.query(Order)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    if status:
        query = query.filter(Order.order_status == status)
    return query.all()


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get single order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}")
def update_order_status(order_id: int, new_status: str, db: Session = Depends(get_db)):
    """Update order status."""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
    
    order.order_status = new_status
    db.commit()
    db.refresh(order)
    return order
