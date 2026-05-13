"""Reports and analytics routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models.order import Order, OrderItem
from backend.models.payment import Payment
from backend.models.product import Product
from backend.models.user import User

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/dashboard-summary")
def dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary with key metrics."""
    total_orders = db.query(func.count(Order.id)).scalar() or 0
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    completed_orders = db.query(func.count(Order.id)).filter(Order.order_status == "delivered").scalar() or 0
    total_customers = db.query(func.count(User.id)).filter(User.role != "owner").scalar() or 0
    
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "completed_orders": completed_orders,
        "total_customers": total_customers,
        "pending_orders": total_orders - completed_orders,
    }


@router.get("/sales-by-category")
def sales_by_category(db: Session = Depends(get_db)):
    """Get sales breakdown by product category."""
    # Join path: Order -> OrderItem -> Product (no direct FK from Order to Product)
    results = db.query(
        Product.category,
        func.count(Order.id).label("order_count"),
        func.sum(Order.total_amount).label("total_amount")
    ).join(
        OrderItem, Order.id == OrderItem.order_id
    ).join(
        Product, OrderItem.product_id == Product.id
    ).group_by(Product.category).all()
    
    return [
        {"category": r[0], "order_count": r[1], "total_amount": r[2]}
        for r in results
    ]


@router.get("/payment-status")
def payment_status(db: Session = Depends(get_db)):
    """Get payment status distribution."""
    results = db.query(
        Order.payment_status,
        func.count(Order.id).label("count")
    ).group_by(Order.payment_status).all()
    
    return [
        {"status": r[0], "count": r[1]}
        for r in results
    ]


@router.get("/retail-vs-wholesale")
def retail_vs_wholesale(db: Session = Depends(get_db)):
    """Get retail vs wholesale sales comparison."""
    retail_revenue = db.query(func.sum(Order.total_amount)).join(
        User, Order.customer_id == User.id
    ).filter(User.role == "retail").scalar() or 0
    
    wholesale_revenue = db.query(func.sum(Order.total_amount)).join(
        User, Order.customer_id == User.id
    ).filter(User.role == "wholesale").scalar() or 0
    
    return {
        "retail_revenue": retail_revenue,
        "wholesale_revenue": wholesale_revenue,
        "total_revenue": retail_revenue + wholesale_revenue,
    }
